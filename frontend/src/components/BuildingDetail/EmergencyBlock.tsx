import { useTranslation } from 'react-i18next';
import type { Building } from '../../types';

interface EmergencyBlockProps {
  buildingData: Building;
  getStatusLabel: (status: string) => string;
}

export function EmergencyBlock({ buildingData, getStatusLabel }: EmergencyBlockProps) {
  const { t } = useTranslation();

  return (
    <div
      className="emergency-block mb-4 fade-in-up"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <h2 className="mb-1">{getStatusLabel(buildingData.verified_status)}</h2>
      <p className="mb-3 fw-normal fs-6">{t('emergency_help_desc')}</p>
      <a
        href="tel:311"
        className="emergency-call-btn"
        aria-label={`${t('call_311_now')} — ${t('call_311_number')}`}
      >
        <span className="me-2" aria-hidden="true">📞</span>{t('call_311_now')} — {t('call_311_number')}
      </a>
      <a
        href={`sms:?body=${encodeURIComponent(`${buildingData.address}: ${t('alert_neighbor_sms_body')}`)}`}
        className="emergency-sms-btn"
      >
        <span className="me-2" aria-hidden="true">💬</span>{t('alert_neighbor')}
      </a>
      <a
        href={`sms:?body=${encodeURIComponent(`${buildingData.address}: ${t('alert_family_sms_body')}`)}`}
        className="emergency-sms-btn"
      >
        <span className="me-2" aria-hidden="true">🏠</span>{t('alert_family')}
      </a>
    </div>
  );
}
