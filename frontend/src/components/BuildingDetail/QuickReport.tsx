import { useTranslation } from 'react-i18next';
import { Row, Col, Button } from 'react-bootstrap';

interface QuickReportProps {
  isReporting: boolean;
  isLoggedIn: boolean;
  onShowAuth?: () => void;
  handleReport: (status: string) => void;
}

export function QuickReport({ isReporting, isLoggedIn, onShowAuth, handleReport }: QuickReportProps) {
  const { t } = useTranslation();

  return (
    <div className="p-3 bg-light rounded-4 border border-primary border-opacity-10 mb-2">
      <h2 className="section-label">{t('quick_report_title')}</h2>
      <Row className="g-2 align-items-stretch">
        <Col xs={4} className="d-flex">
          <Button
            variant="success"
            disabled={isReporting}
            aria-label={t('status_up')}
            className="w-100 py-3 fw-bold shadow-sm d-flex flex-column align-items-center justify-content-center h-100 border-0"
            onClick={() => handleReport('UP')}
          >
            <div className="bg-white rounded-circle p-1 mb-2 shadow-sm d-flex align-items-center justify-content-center" style={{ width: '32px', height: '32px' }}>
              <span className="fs-5" aria-hidden="true">✅</span>
            </div>
            <span className="fw-bold">{t('btn_report_working')}</span>
          </Button>
        </Col>
        <Col xs={4} className="d-flex">
          <Button
            variant="danger"
            disabled={isReporting}
            aria-label={t('status_down')}
            className="w-100 py-3 fw-bold shadow-sm d-flex flex-column align-items-center justify-content-center h-100 border-0"
            onClick={() => handleReport('DOWN')}
          >
            <div className="bg-white rounded-circle p-1 mb-2 shadow-sm d-flex align-items-center justify-content-center" style={{ width: '32px', height: '32px' }}>
              <span className="fs-5" aria-hidden="true">❌</span>
            </div>
            <span className="fw-bold">{t('btn_report_not_working')}</span>
          </Button>
        </Col>
        <Col xs={4} className="d-flex">
          <Button
            variant="warning"
            disabled={isReporting}
            aria-label={t('status_slow')}
            className="w-100 py-3 fw-bold shadow-sm text-dark d-flex flex-column align-items-center justify-content-center h-100 border-0"
            onClick={() => handleReport('SLOW')}
          >
            <div className="bg-dark rounded-circle p-1 mb-2 shadow-sm d-flex align-items-center justify-content-center" style={{ width: '32px', height: '32px' }}>
              <span className="fs-5" aria-hidden="true">⚠️</span>
            </div>
            <span className="fw-bold">{t('btn_report_slow')}</span>
          </Button>
        </Col>
      </Row>
      <p className="mb-0 mt-3 text-muted small">{t('quick_report_help')}</p>
      <p className="mb-0 mt-1 text-muted small">{t('verification_explainer')}</p>

      {/* Emergency reports */}
      <div className="mt-3 pt-3 border-top border-danger border-opacity-25">
        <h3 className="section-label mt-1">
          <span aria-hidden="true">🚨</span> {t('emergency_reports')}
        </h3>
        <Row className="g-2">
          <Col xs={12} sm={6} className="d-flex">
            <Button
              variant="danger"
              disabled={isReporting}
              aria-label={t('status_trapped')}
              className="w-100 py-2 fw-bold shadow-sm d-flex align-items-center justify-content-center gap-2 border-0"
              onClick={() => handleReport('TRAPPED')}
            >
              <span aria-hidden="true">🆘</span>
              <span>{t('status_trapped_label')}</span>
            </Button>
          </Col>
          <Col xs={12} sm={6} className="d-flex">
            <Button
              variant="danger"
              disabled={isReporting}
              aria-label={t('status_unsafe')}
              className="w-100 py-2 fw-bold d-flex align-items-center justify-content-center gap-2"
              onClick={() => handleReport('UNSAFE')}
            >
              <span aria-hidden="true">⚠️</span>
              <span>{t('status_unsafe_label')}</span>
            </Button>
          </Col>
        </Row>
        <p className="mb-0 mt-2 text-dark small fw-bold">{t('emergency_reports_note')}</p>
      </div>

      {/* Logged-out inline CTA */}
      {!isLoggedIn && (
        <div className="mt-3 pt-3 border-top d-flex align-items-center justify-content-between gap-3 flex-wrap">
          <small className="text-muted">{t('report_login_cta')}</small>
          <Button
            variant="primary"
            size="sm"
            className="rounded-pill px-3 fw-bold flex-shrink-0"
            onClick={onShowAuth}
          >
            {t('sign_in')}
          </Button>
        </div>
      )}
    </div>
  );
}
