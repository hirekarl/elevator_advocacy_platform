import { Row, Col, Alert } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { HeroSearch } from '../HeroSearch';
import { BuildingsMap } from '../BuildingsMap';
import { PrimaryBuildingBanner } from './PrimaryBuildingBanner';
import { AdvocacySections } from './AdvocacySections';

interface LandingPageProps {
  onSearch: (e?: React.FormEvent) => void;
  searchData: { house_number: string; street: string; borough: string };
  setSearchData: (data: { house_number: string; street: string; borough: string }) => void;
  isPending: boolean;
  searchError: string;
  isLoggedIn: boolean;
  username: string;
  primaryBuildingBin: string | null;
  primaryBuildingStatus: string | null;
  getStatusPillClass: (status: string) => string;
  getStatusShortLabel: (status: string) => string;
}

export function LandingPage({
  onSearch,
  searchData,
  setSearchData,
  isPending,
  searchError,
  isLoggedIn,
  username,
  primaryBuildingBin,
  primaryBuildingStatus,
  getStatusPillClass,
  getStatusShortLabel
}: LandingPageProps) {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <>
      <HeroSearch
        onSearch={onSearch}
        searchData={searchData}
        setSearchData={setSearchData}
        isPending={isPending}
      />
      <div className="container pb-5 px-3">
        {searchError && (
          <Alert variant="danger" className="mt-3" role="alert">
            {searchError}
          </Alert>
        )}

        {/* State C: logged in + primary building set */}
        {isLoggedIn && primaryBuildingBin && (
          <PrimaryBuildingBanner
            username={username}
            primaryBuildingBin={primaryBuildingBin}
            primaryBuildingStatus={primaryBuildingStatus}
            getStatusPillClass={getStatusPillClass}
            getStatusShortLabel={getStatusShortLabel}
          />
        )}

        {/* State B: logged in, no primary building */}
        {isLoggedIn && !primaryBuildingBin && (
          <Alert variant="info" className="mt-4 rounded-4 border-0 shadow-sm">
            <strong>{t('welcome_back')}, {username}.</strong> {t('set_primary_prompt')}
          </Alert>
        )}
      </div>

      <div className="container pb-5 px-3">
        <Row className="mt-4 mt-md-5">
          <Col md={12} lg={10} className="mx-auto text-center mb-5">
            <h2 className="fw-bold mb-4 px-3 fs-3 fs-md-2">{t('explore_outages')}</h2>
            <div className="px-1 px-md-2">
              <BuildingsMap onBuildingSelect={(binId) => navigate(`/building/${binId}`)} />
            </div>
          </Col>
        </Row>
      </div>

      <AdvocacySections />
    </>
  );
}
