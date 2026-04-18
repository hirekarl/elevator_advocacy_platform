import { Alert } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';

import type { Building, OptimisticReport } from '../types';

// Hooks
import { useBuildingAdvocacy } from '../hooks/useBuildingAdvocacy';

// Sub-components
import { EmergencyBlock } from './BuildingDetail/EmergencyBlock';
import { QuickReport } from './BuildingDetail/QuickReport';
import { BuildingMetrics } from './BuildingDetail/BuildingMetrics';
import { ExecutiveSummary as ExecutiveSummaryComponent } from './BuildingDetail/ExecutiveSummary';
import { AdvocacyScript as AdvocacyScriptComponent } from './BuildingDetail/AdvocacyScript';
import { PaperTrail } from './BuildingDetail/PaperTrail';
import { AdvocacyTools } from './BuildingDetail/AdvocacyTools';
import { NewsSection } from './BuildingDetail/NewsSection';
import { AdvocacyModal } from './BuildingDetail/AdvocacyModal';
import { ToastNotifier } from './BuildingDetail/ToastNotifier';
import { StatusHeader } from './BuildingDetail/StatusHeader';
import { ComplaintHistory } from './BuildingDetail/ComplaintHistory';

interface BuildingDetailProps {
  buildingData: Building;
  isLoggedIn?: boolean;
  onShowAuth?: () => void;
  onReportOptimistic?: (report: OptimisticReport) => void;
  refreshBuilding?: () => void;
}

export function BuildingDetail({
  buildingData,
  isLoggedIn = false,
  onShowAuth,
  onReportOptimistic,
  refreshBuilding
}: BuildingDetailProps) {
  const { t } = useTranslation();

  const {
    advocacyScript,
    executiveSummary,
    isLoadingScript,
    isLoadingSummary,
    isReporting,
    isRefreshingNews,
    showToast,
    setShowToast,
    toastMessage,
    toastVariant,
    showAdvocacyModal,
    setShowAdvocacyModal,
    advocacyFormData,
    setAdvocacyFormData,
    isSubmittingLog,
    handleReport,
    handleLogAdvocacy,
    handleRefreshNews,
    handleCopySummary,
    handleCopyScript,
    fetchExecutiveSummary,
    triggerToast
  } = useBuildingAdvocacy({
    buildingData,
    onReportOptimistic,
    refreshBuilding,
    onShowAuth
  });

  if (!buildingData) return null;

  const getStatusRibbonClass = (status: string): string => {
    if (['DOWN', 'TRAPPED', 'UNSAFE'].includes(status)) return 'ribbon-danger';
    if (['UNVERIFIED', 'SLOW'].includes(status)) return 'ribbon-warning';
    return 'ribbon-success';
  };

  const getStatusLabel = (status: string): string => {
    const labels: Record<string, string> = {
      DOWN: t('status_label_down'),
      TRAPPED: t('status_label_trapped'),
      UNSAFE: t('status_label_unsafe'),
      UNVERIFIED: t('status_label_unverified'),
      UP: t('status_label_up'),
      SLOW: t('status_label_slow'),
    };
    return labels[status] ?? status;
  };

  const isEmergency = (['DOWN', 'TRAPPED', 'UNSAFE'] as string[]).includes(buildingData.verified_status);

  return (
    <div className="building-action-center pb-safe">
      {/* Mock Data Warning */}
      {buildingData.is_mocked && (
        <Alert variant="warning" className="border-0 rounded-0 mb-0 py-2 text-center fw-bold small shadow-sm animate-pulse">
          <span aria-hidden="true">🧪</span> {t('dev_mode_mock_data')}
        </Alert>
      )}

      {/* 311 Log Modal */}
      <AdvocacyModal
        show={showAdvocacyModal}
        onHide={() => setShowAdvocacyModal(false)}
        formData={advocacyFormData}
        setFormData={setAdvocacyFormData}
        onSubmit={handleLogAdvocacy}
        isSubmitting={isSubmittingLog}
      />

      <ToastNotifier
        show={showToast}
        onClose={() => setShowToast(false)}
        message={toastMessage}
        variant={toastVariant}
      />

      {/* Martha Mode: Emergency block — shown first when elevator is critically impacted */}
      {isEmergency && (
        <EmergencyBlock
          buildingData={buildingData}
          getStatusLabel={getStatusLabel}
        />
      )}

      {/* Martha Mode: Unverified status plain-language alert */}
      {buildingData.verified_status === 'UNVERIFIED' && (
        <Alert
          variant="warning"
          className="rounded-4 shadow-sm mb-4 py-3 border-warning border-2"
          role="status"
          aria-live="polite"
        >
          <div className="fw-bold fs-6 mb-1">{t('status_label_unverified')}</div>
          <div className="small">{t('verification_neighbor_prompt')}</div>
        </Alert>
      )}

      {/* ZONE 1: Identity & Live Status */}
      <StatusHeader
        buildingData={buildingData}
        isLoggedIn={isLoggedIn}
        getStatusRibbonClass={getStatusRibbonClass}
        getStatusLabel={getStatusLabel}
        onTriggerToast={triggerToast}
      />

      <div className="px-4 pb-4">
        <QuickReport
          isReporting={isReporting}
          isLoggedIn={isLoggedIn}
          onShowAuth={onShowAuth}
          handleReport={handleReport}
        />
      </div>

      {/* In emergency states, analytics render after the advocacy tools below */}
      {!isEmergency && (
        <>
          <BuildingMetrics buildingData={buildingData} />
          <ExecutiveSummaryComponent
            executiveSummary={executiveSummary}
            isLoadingSummary={isLoadingSummary}
            onRefresh={fetchExecutiveSummary}
          />
          <div className="px-4">
            <ComplaintHistory complaints={buildingData.soda_complaints ?? []} />
          </div>
        </>
      )}

      {/* ZONE 3: Advocacy Center */}
      <h2 className="fw-bold mb-3 mt-5 d-flex align-items-center fs-4">
        <span className="me-2" aria-hidden="true">📢</span> {t('advocacy_center')}
      </h2>

      {/* 311 call — only in non-emergency (emergency block handles it above) */}
      {!isEmergency && (
        <a
          href="tel:311"
          className="d-flex align-items-center justify-content-between p-3 mb-3 bg-danger text-white rounded-4 text-decoration-none fw-bold shadow-sm"
          aria-label={`${t('call_311_now')} — ${t('call_311_number')}`}
        >
          <div>
            <div className="fs-6"><span aria-hidden="true">📞</span> {t('call_311_now')}</div>
            <small className="fw-normal">{t('call_311_desc')}</small>
          </div>
          <div className="text-end">
            <div className="fw-bold">{t('call_311_number')}</div>
            <small className="fw-normal">{t('or_dial_311')}</small>
          </div>
        </a>
      )}

      <AdvocacyScriptComponent
        advocacyScript={advocacyScript}
        isLoadingScript={isLoadingScript}
        isEmergency={isEmergency}
        isLoggedIn={isLoggedIn}
        onShowAdvocacyModal={() => setShowAdvocacyModal(true)}
        onCopy={handleCopyScript}
      />

      {/* Analytics — deferred below advocacy tools in emergency states */}
      {isEmergency && (
        <>
          <BuildingMetrics buildingData={buildingData} />
          <ExecutiveSummaryComponent
            executiveSummary={executiveSummary}
            isLoadingSummary={isLoadingSummary}
            onRefresh={fetchExecutiveSummary}
          />
          <div className="px-4">
            <ComplaintHistory complaints={buildingData.soda_complaints ?? []} />
          </div>
        </>
      )}

      <PaperTrail
        buildingData={buildingData}
        isLoggedIn={isLoggedIn}
        isEmergency={isEmergency}
        onShowAdvocacyModal={() => setShowAdvocacyModal(true)}
      />

      <AdvocacyTools
        buildingData={buildingData}
        onCopySummary={handleCopySummary}
      />

      <NewsSection
        buildingData={buildingData}
        isRefreshingNews={isRefreshingNews}
        onRefreshNews={handleRefreshNews}
      />
    </div>
  );
}
