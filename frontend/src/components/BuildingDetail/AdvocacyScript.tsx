import { useTranslation } from 'react-i18next';
import { Card, Button } from 'react-bootstrap';
import type { AdvocacyScript as AdvocacyScriptType } from '../../types';

interface AdvocacyScriptProps {
  advocacyScript: AdvocacyScriptType | null;
  isLoadingScript: boolean;
  isEmergency: boolean;
  isLoggedIn: boolean;
  onShowAdvocacyModal: () => void;
  onCopy: (text: string) => void;
}

export function AdvocacyScript({
  advocacyScript,
  isLoadingScript,
  isEmergency,
  isLoggedIn,
  onShowAdvocacyModal,
  onCopy
}: AdvocacyScriptProps) {
  const { t } = useTranslation();

  return (
    <Card className="border-0 shadow-sm mb-4 overflow-hidden rounded-4 text-white script-card">
      <Card.Body className="p-4">
        {isLoadingScript ? (
          <div className="py-2 d-flex align-items-center gap-3">
            <div
              className="spinner-border spinner-border-sm text-white"
              role="status"
              aria-label={t('generating_strategy')}
            />
            <span className="text-white small fw-bold" aria-hidden="true">{t('generating_strategy')}</span>
          </div>
        ) : advocacyScript ? (
          <>
            <div className="d-flex justify-content-between align-items-start mb-3">
              <p className="mb-1 fw-semibold text-white" style={{ opacity: 0.55, fontSize: '0.65rem', letterSpacing: '0.1em', textTransform: 'uppercase' }}>
                {isEmergency ? t('script_label_emergency') : t('script_label_standard')}
              </p>
              <h3 className="fw-bold text-white mb-0 fs-6">{advocacyScript.headline}</h3>
              {isLoggedIn && (
                <Button
                  variant="info"
                  size="sm"
                  className="rounded-pill px-3 fw-bold text-white shadow-sm"
                  onClick={onShowAdvocacyModal}
                >
                  <span aria-hidden="true">📝</span> {t('log_this_call')}
                </Button>
              )}
            </div>
            <div className="p-3 bg-white text-dark rounded-3 border-start border-info border-5 mb-3 shadow-sm">
              <div className="mb-0 small" style={{ whiteSpace: 'pre-wrap' }}>
                {advocacyScript.script}
              </div>
            </div>
            <div className="d-flex flex-column flex-sm-row justify-content-between align-items-center gap-3">
              <small className="text-white">Legal: {advocacyScript.legal_reference}</small>
              <Button
                variant="light"
                size="sm"
                className="rounded-pill px-4 fw-bold shadow-sm"
                onClick={() => onCopy(advocacyScript.script)}
              >
                {t('copy_script')}
              </Button>
            </div>
          </>
        ) : (
          <p className="mb-0 text-white">{t('no_strategy_available')}</p>
        )}
      </Card.Body>
    </Card>
  );
}
