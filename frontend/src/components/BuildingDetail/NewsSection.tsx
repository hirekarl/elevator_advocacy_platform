import { useTranslation } from 'react-i18next';
import { Row, Col, Card, Badge, Alert, Button } from 'react-bootstrap';
import type { Building } from '../../types';

interface NewsSectionProps {
  buildingData: Building;
  isRefreshingNews: boolean;
  onRefreshNews: () => void;
}

export function NewsSection({ buildingData, isRefreshingNews, onRefreshNews }: NewsSectionProps) {
  const { t } = useTranslation();

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-4 mt-5">
        <h2 className="fw-bold mb-0 fs-4">
          <span aria-hidden="true">📰</span> {t('news_section')}
        </h2>
        <Button
          variant="secondary"
          size="sm"
          className="rounded-pill px-3 fw-bold"
          aria-label={`${t('refresh')} ${t('news_section')}`}
          disabled={isRefreshingNews}
          onClick={onRefreshNews}
        >
          {isRefreshingNews ? (
            <>
              <span className="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true" />
              {t('syncing')}
            </>
          ) : t('refresh')}
        </Button>
      </div>

      <Row className="g-3">
        {buildingData.news_articles && buildingData.news_articles.length > 0 ? (
          buildingData.news_articles.map((article) => (
            <Col md={6} key={article.url}>
              <Card className="h-100 border-0 shadow-sm rounded-4">
                <Card.Body className="p-3">
                  <div className="d-flex justify-content-between mb-2">
                    <div className="d-flex align-items-center gap-2">
                      <small className="text-primary fw-bold text-uppercase fs-8">{article.source}</small>
                      {article.is_mocked && (
                        <Badge bg="secondary" className="fs-10 text-uppercase fw-bold opacity-75">Mock</Badge>
                      )}
                    </div>
                    <small className="text-muted fs-8">{article.published_date}</small>
                  </div>
                  <h6 className="fw-bold mb-2">{article.title}</h6>
                  <p className="text-muted fs-8 mb-3">{article.summary}</p>
                  <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-link p-0 fs-8 fw-bold"
                    aria-label={`${t('read_full_story')}: ${article.title}`}
                  >
                    {t('read_full_story')} →
                  </a>
                </Card.Body>
              </Card>
            </Col>
          ))
        ) : (
          <Col xs={12}>
            <Alert variant="light" className="border-dashed py-4 text-center text-muted small">
              {t('no_media_mentions')}
            </Alert>
          </Col>
        )}
      </Row>
    </>
  );
}
