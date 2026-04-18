import { useState } from 'react';
import { Badge, Alert } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import type { SodaComplaint } from '../../types';

const CATEGORY_LABELS: Record<string, string> = {
  '6S': 'Elevator Complaint',
  '6M': 'Elevator / Escalator',
};

const COLLAPSED_LIMIT = 5;

interface ComplaintHistoryProps {
  complaints: SodaComplaint[];
}

function statusVariant(status: string | undefined): string {
  if (!status) return 'secondary';
  const s = status.toLowerCase();
  if (s === 'open') return 'warning';
  if (s === 'closed') return 'success';
  return 'secondary';
}

export function ComplaintHistory({ complaints }: ComplaintHistoryProps) {
  const { t } = useTranslation();
  const [expanded, setExpanded] = useState(false);

  if (!complaints || complaints.length === 0) {
    return (
      <>
        <h2 className="fw-bold mb-3 mt-5 fs-4">
          <span aria-hidden="true">📋</span> {t('complaint_history_title')}
        </h2>
        <Alert
          variant="light"
          className="border-dashed py-4 text-center text-muted small"
        >
          {t('complaint_history_empty')}
        </Alert>
      </>
    );
  }

  const visible = expanded ? complaints : complaints.slice(0, COLLAPSED_LIMIT);
  const hasMore = complaints.length > COLLAPSED_LIMIT;

  return (
    <>
      <h2 className="fw-bold mb-3 mt-5 fs-4">
        <span aria-hidden="true">📋</span> {t('complaint_history_title')}
      </h2>
      <ul className="list-unstyled mb-0" aria-label={t('complaint_history_title')}>
        {visible.map((c, i) => (
          <li
            key={c.complaint_number ?? i}
            className="d-flex flex-column gap-1 py-3 border-bottom"
          >
            <div className="d-flex align-items-center justify-content-between gap-2 flex-wrap">
              <span className="fw-semibold small">
                {CATEGORY_LABELS[c.complaint_category] ?? c.complaint_category}
                {c.complaint_number && (
                  <span className="text-muted fw-normal ms-2">#{c.complaint_number}</span>
                )}
              </span>
              <div className="d-flex align-items-center gap-2">
                {c.status && (
                  <Badge bg={statusVariant(c.status)} className="text-capitalize">
                    {c.status}
                  </Badge>
                )}
                <small className="text-muted">
                  {t('complaint_history_filed')}: {c.date_entered}
                </small>
              </div>
            </div>
            {c.inspection_date && (
              <small className="text-muted">
                {t('complaint_history_inspected')}: {c.inspection_date}
              </small>
            )}
            {c.disposition_date && (
              <small className="text-muted">
                {t('complaint_history_resolved')}: {c.disposition_date}
              </small>
            )}
          </li>
        ))}
      </ul>
      {hasMore && (
        <button
          type="button"
          className="btn btn-link p-0 mt-2 small fw-bold"
          onClick={() => setExpanded(prev => !prev)}
          aria-expanded={expanded}
        >
          {expanded
            ? t('complaint_history_show_less')
            : t('complaint_history_show_all', { count: complaints.length })}
        </button>
      )}
    </>
  );
}
