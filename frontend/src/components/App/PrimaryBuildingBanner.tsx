import { Button } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';

interface PrimaryBuildingBannerProps {
  username: string;
  primaryBuildingBin: string;
  primaryBuildingStatus: string | null;
  getStatusPillClass: (status: string) => string;
  getStatusShortLabel: (status: string) => string;
}

export function PrimaryBuildingBanner({
  username,
  primaryBuildingBin,
  primaryBuildingStatus,
  getStatusPillClass,
  getStatusShortLabel
}: PrimaryBuildingBannerProps) {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <div className="d-flex flex-column flex-sm-row align-items-start align-items-sm-center justify-content-between gap-3 mt-4 p-4 rounded-4 shadow-sm home-building-banner">
      <div>
        <div className="fw-bold text-white fs-5 home-building-title">
          {t('welcome_back')}, {username}
        </div>
        <div className="d-flex align-items-center gap-2 mt-2">
          {primaryBuildingStatus && (
            <span className={`px-2 py-1 rounded-pill home-status-pill ${getStatusPillClass(primaryBuildingStatus)}`}>
              {getStatusShortLabel(primaryBuildingStatus)}
            </span>
          )}
          <span className="text-white home-building-subtitle">
            {t('your_home_building_prompt')}
          </span>
        </div>
      </div>
      <Button
        onClick={() => navigate(`/building/${primaryBuildingBin}`)}
        className="btn-amber rounded-pill px-4 py-2 flex-shrink-0"
      >
        {t('go_to_my_building')} →
      </Button>
    </div>
  );
}
