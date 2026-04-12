from datetime import date
from unittest.mock import MagicMock, patch

from django.test import TestCase

from services.news_search import NewsArticleSchema, NewsSearchService

from .models import Building, BuildingNews
from .tasks import fetch_building_news


class NewsSearchServiceTests(TestCase):
    """
    Unit tests for Kiran's News Search Service.
    """

    def setUp(self):
        self.service = NewsSearchService()
        self.address = "123 Broadway, Manhattan, NY"

    @patch('serpapi.Client')
    @patch('google.genai.Client')
    def test_search_and_extract_success(self, mock_genai_client, mock_serp_client):
        """
        Tests the full search and extraction pipeline with mocked APIs.
        """
        # 1. Mock SerpAPI Response
        mock_serp_instance = mock_serp_client.return_value
        mock_serp_instance.search.return_value = {
            "organic_results": [
                {
                    "title": "Elevator Outage at 123 Broadway",
                    "link": "https://gothamist.com/news/123-broadway-outage",
                    "snippet": "Residents are stranded after all elevators failed at 123 Broadway."
                }
            ]
        }

        # 2. Mock Gemini GenAI Response
        mock_genai_instance = mock_genai_client.return_value
        mock_response = MagicMock()
        # Mocking the parsed attribute (Pydantic model)
        mock_response.parsed = NewsArticleSchema(
            title="Elevator Outage at 123 Broadway",
            url="https://gothamist.com/news/123-broadway-outage",
            source="Gothamist",
            published_date=date(2026, 4, 1),
            summary="Residents are stranded after all elevators failed.",
            relevance_score=0.95
        )
        mock_genai_instance.models.generate_content.return_value = mock_response

        # 3. Execute
        # We need to ensure API keys are "present" for the service to not use mocks
        with patch.dict('os.environ', {'SERPAPI_KEY': 'fake_serp', 'GEMINI_API_KEY': 'fake_gemini'}):
            self.service.serp_api_key = 'fake_serp'
            self.service.gemini_api_key = 'fake_gemini'
            self.service.client = mock_genai_instance # Inject mock client
            
            articles = self.service.search_and_extract(self.address)

        # 4. Assertions
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Elevator Outage at 123 Broadway")
        self.assertEqual(articles[0].relevance_score, 0.95)

class NewsTaskTests(TestCase):
    """
    Integration tests for the fetch_building_news background task.
    """

    def setUp(self):
        self.building = Building.objects.create(
            bin="1112223",
            address="456 Park Ave",
            borough="Manhattan"
        )

    @patch('services.news_search.NewsSearchService.search_and_extract')
    def test_fetch_building_news_task(self, mock_search):
        """
        Tests that the task correctly saves articles to the database.
        """
        # 1. Mock Service Output
        mock_search.return_value = [
            NewsArticleSchema(
                title="Park Ave Elevator Crisis",
                url="https://thecity.nyc/park-ave-outage",
                source="The City",
                published_date=date(2026, 3, 15),
                summary="A major elevator crisis is unfolding at 456 Park Ave.",
                relevance_score=0.88
            ),
            NewsArticleSchema(
                title="Unrelated News",
                url="https://example.com/unrelated",
                source="Example",
                published_date=date(2026, 3, 10),
                summary="Something about a park, but not elevators.",
                relevance_score=0.2  # Should be skipped by task
            )
        ]

        # 2. Run Task (Synchronously using the underlying function)
        fetch_building_news.func(bin=self.building.bin)

        # 3. Assertions
        news_count = BuildingNews.objects.filter(building=self.building).count()
        self.assertEqual(news_count, 1)
        
        saved_article = BuildingNews.objects.get(building=self.building)
        self.assertEqual(saved_article.title, "Park Ave Elevator Crisis")
        self.assertEqual(saved_article.relevance_score, 0.88)
