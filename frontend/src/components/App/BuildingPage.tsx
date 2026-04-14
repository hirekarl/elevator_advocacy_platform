import { Container, Row, Col, Button } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import type { Building, OptimisticReport, AuthSuccessData } from '../../types';
import { BuildingDetail } from '../BuildingDetail';
import { BuildingFeed } from './BuildingFeed';
import { SignupForm } from '../AuthForms';

interface BuildingPageProps {
  activeBuilding: Building;
  isLoggedIn: boolean;
  onShowAuthModal: () => void;
  onAuthSuccess: (data: AuthSuccessData) => void;
  onReportOptimistic: (report: OptimisticReport) => void;
  onRefreshBuilding: (binId: string) => void;
  optimisticReports: OptimisticReport[];
}

export function BuildingPage({
  activeBuilding,
  isLoggedIn,
  onShowAuthModal,
  onAuthSuccess,
  onReportOptimistic,
  onRefreshBuilding,
  optimisticReports
}: BuildingPageProps) {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <Container className="mt-3 mt-md-4 pb-5 px-3">
      <Button
        variant="link"
        className="text-decoration-none mb-3 p-0 d-flex align-items-center text-muted fw-bold"
        onClick={() => navigate('/')}
      >
        <span className="me-2" aria-hidden="true">←</span> {t('search_address')}
      </Button>

      <Row className="g-4">
        <Col lg={7}>
          <BuildingDetail
            buildingData={activeBuilding}
            isLoggedIn={isLoggedIn}
            onShowAuth={onShowAuthModal}
            onReportOptimistic={onReportOptimistic}
            refreshBuilding={() => onRefreshBuilding(activeBuilding.bin)}
          />
        </Col>
        <Col lg={5}>
          <div className="sticky-lg-top" style={{ top: '100px', zIndex: 10 }}>
            {!isLoggedIn && (
              <SignupForm onSuccess={onAuthSuccess} />
            )}

            <div className={!isLoggedIn ? 'mt-4' : ''}>
              <BuildingFeed optimisticReports={optimisticReports} />
            </div>
          </div>
        </Col>
      </Row>
    </Container>
  );
}
