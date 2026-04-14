import { useTranslation } from 'react-i18next';
import { Card, Row, Col, Button } from 'react-bootstrap';
import type { Building } from '../../types';

interface AdvocacyToolsProps {
  buildingData: Building;
  onCopySummary: () => void;
}

export function AdvocacyTools({ buildingData, onCopySummary }: AdvocacyToolsProps) {
  const { t } = useTranslation();
  const lossOfService = buildingData.loss_of_service_30d;

  return (
    <Card className="border-0 shadow-sm mb-5 bg-white rounded-4">
      <Card.Body className="p-4">
        <Row className="align-items-center">
          <Col md={8}>
            <h2 className="fw-bold mb-2 fs-5">{t('help_advocate_title')}</h2>
            <p className="text-dark mb-0 small fw-bold">{t('help_advocate_desc')}</p>
          </Col>
          <Col md={4} className="text-md-end mt-3 mt-md-0">
            <Button
              variant="outline-primary"
              className="fw-bold rounded-pill px-4 w-100 w-md-auto mb-2"
              onClick={onCopySummary}
            >
              {t('copy_summary')}
            </Button>
            <div className="d-flex flex-wrap gap-2 justify-content-md-end">
              <a
                href={`https://wa.me/?text=${encodeURIComponent(`Elevator Advocacy Report: ${buildingData.address}\n- 30-Day Service Loss: ${lossOfService != null ? `${lossOfService}%` : '—'}\n- Current Status: ${buildingData.verified_status}`)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="badge bg-dark px-3 py-2 fw-medium rounded-pill text-decoration-none"
                aria-label="Share building status via WhatsApp"
              >
                Share via WhatsApp
              </a>
              {buildingData.representative?.email ? (
                <a
                  href={`mailto:${buildingData.representative.email}?subject=${encodeURIComponent(`Elevator Outage: ${buildingData.address}`)}&body=${encodeURIComponent(`Dear ${buildingData.representative.name},\n\nI am writing to you today to report a persistent elevator issue at ${buildingData.address}.\n\nAccording to the Elevator Advocacy Platform, this building has a 30-day "Loss of Service" metric of ${lossOfService != null ? `${lossOfService}%` : 'unknown'}.\n\nThe current verified status of the elevator is: ${buildingData.verified_status}.\n\nPlease help us hold the building management accountable for these service interruptions.\n\nThank you,\nA concerned neighbor`)}`}
                  className="badge bg-dark px-3 py-2 fw-medium rounded-pill text-decoration-none"
                  aria-label={`Email ${buildingData.representative.name}`}
                  rel="noopener noreferrer"
                >
                  Email {buildingData.representative.name}
                </a>
              ) : buildingData.representative?.phone ? (
                <a
                  href={`tel:${buildingData.representative.phone}`}
                  className="badge bg-dark px-3 py-2 fw-medium rounded-pill text-decoration-none"
                  aria-label={`Call ${buildingData.representative.name}`}
                  rel="noopener noreferrer"
                >
                  Call {buildingData.representative.name}
                </a>
              ) : (
                <a
                  href={`mailto:?subject=${encodeURIComponent(`Elevator Issue: ${buildingData.address}`)}&body=${encodeURIComponent(`Elevator Advocacy Report: ${buildingData.address}\n- 30-Day Service Loss: ${lossOfService != null ? `${lossOfService}%` : '—'}\n- Current Status: ${buildingData.verified_status}`)}`}
                  className="badge bg-dark px-3 py-2 fw-medium rounded-pill text-decoration-none"
                  aria-label="Email building status to a representative"
                  rel="noopener noreferrer"
                >
                  Email Representative
                </a>
              )}
            </div>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
}
