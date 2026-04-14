import { Badge, Alert } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import type { OptimisticReport } from '../../types';

interface BuildingFeedProps {
  optimisticReports: OptimisticReport[];
}

export function BuildingFeed({ optimisticReports }: BuildingFeedProps) {
  const { t } = useTranslation();

  return (
    <div className="p-4 bg-white border rounded shadow-sm">
      <h2 className="mb-3 d-flex justify-content-between align-items-center fs-5">
        {t('building_feed')}
        {optimisticReports.length > 0 && (
          <Badge bg="primary" pill>{optimisticReports.length}</Badge>
        )}
      </h2>
      {optimisticReports.length === 0 ? (
        <Alert variant="light" className="text-muted border border-secondary border-opacity-25 border-dashed">
          {t('no_recent_activity')}
        </Alert>
      ) : (
        <div style={{ maxHeight: '400px', overflowY: 'auto' }} className="pe-2">
          {optimisticReports.map((report) => (
            <div
              key={report.id}
              className={`card mb-3 shadow-sm ${report.pending ? 'border-warning animate-pulse' : 'border-success'}`}
            >
              <div className="card-body p-3">
                <h6 className="card-title small fw-bold mb-1">
                  {report.pending ? t('verification_pending') : t('verified_status')}
                </h6>
                <p className="card-text small mb-0">
                  {report.status} — {report.reported_at || report.time}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
