import { useTranslation } from 'react-i18next';
import { Row, Col } from 'react-bootstrap';
import type { Building } from '../../types';

interface BuildingMetricsProps {
  buildingData: Building;
}

export function BuildingMetrics({ buildingData }: BuildingMetricsProps) {
  const { t } = useTranslation();

  const lossOfService = buildingData.loss_of_service_30d;
  const uptimePct = lossOfService != null ? 100 - lossOfService : null;
  const riskScore = buildingData.failure_risk?.risk_score ?? null;

  return (
    <Row className="g-3 mb-4">
      <Col xs={12} md={6}>
        <div className={`p-3 bg-white shadow-sm rounded-4 border h-100 metric-card ${uptimePct != null ? (lossOfService! > 10 ? 'mc-warn' : 'mc-good') : 'mc-neutral'}`}>
          <h2 className="section-label">{t('loss_of_service')}</h2>
          <div className="d-flex align-items-end mb-2">
            <span className="metric-value me-2">
              {uptimePct != null ? `${uptimePct}%` : '—'}
            </span>
            <span className="text-muted mb-1 pb-1 small">{t('uptime_30d')}</span>
          </div>
          {uptimePct != null && (
            <div className="progress" style={{ height: '8px' }}>
              <div
                className={`progress-bar bg-${lossOfService! > 10 ? 'warning' : 'success'}`}
                role="progressbar"
                style={{ width: `${uptimePct}%` }}
                aria-valuenow={uptimePct}
                aria-valuemin={0}
                aria-valuemax={100}
                aria-label={t('loss_of_service')}
              ></div>
            </div>
          )}
        </div>
      </Col>
      <Col xs={12} md={6}>
        <div className={`p-3 bg-white shadow-sm rounded-4 border h-100 metric-card ${riskScore != null ? (riskScore > 60 ? 'mc-danger' : riskScore > 30 ? 'mc-warn' : 'mc-good') : 'mc-neutral'}`}>
          <h2 className="section-label">{t('maintenance_forecast')}</h2>
          <div className="d-flex align-items-end mb-2">
            <span className="metric-value me-2">
              {riskScore != null ? `${riskScore}%` : '—'}
            </span>
            <span className="text-muted mb-1 pb-1 small">{t('risk_level')}</span>
          </div>
          {riskScore != null && (
            <div className="progress" style={{ height: '8px' }}>
              <div
                className={`progress-bar bg-${riskScore > 60 ? 'danger' : 'warning'}`}
                role="progressbar"
                style={{ width: `${riskScore}%` }}
                aria-valuenow={riskScore}
                aria-valuemin={0}
                aria-valuemax={100}
                aria-label={t('maintenance_forecast')}
              ></div>
            </div>
          )}
        </div>
      </Col>
    </Row>
  );
}
