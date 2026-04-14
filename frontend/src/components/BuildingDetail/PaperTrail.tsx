import { useTranslation } from 'react-i18next';
import { Card, Row, Col, ListGroup, Badge, Alert, Button } from 'react-bootstrap';
import type { Building } from '../../types';

interface PaperTrailProps {
  buildingData: Building;
  isLoggedIn: boolean;
  isEmergency: boolean;
  onShowAdvocacyModal: () => void;
}

export function PaperTrail({ buildingData, isLoggedIn, isEmergency, onShowAdvocacyModal }: PaperTrailProps) {
  const { t } = useTranslation();

  const tenantReports = buildingData.recent_reports?.filter(r => !r.is_official) || [];
  const officialReports = buildingData.recent_reports?.filter(r => r.is_official) || [];
  const advocacyLogs = buildingData.advocacy_logs || [];

  return (
    <Card className="border-0 shadow-sm mb-4 rounded-4 overflow-hidden">
      <Card.Header className="bg-white border-0 pt-4 px-4 d-flex justify-content-between align-items-center">
        <h2 className="fw-bold mb-0 fs-5">
          <span className="me-2" aria-hidden="true">📜</span> {t('paper_trail_title')}
        </h2>
        {isLoggedIn && !isEmergency && (
          <Button
            variant="primary"
            size="sm"
            className="rounded-pill px-3 fw-bold shadow-sm"
            onClick={onShowAdvocacyModal}
          >
            + {t('log_311_title')}
          </Button>
        )}
      </Card.Header>
      <Card.Body className="px-4 pb-4">
        <Row className="g-4">
          <Col lg={12}>
            <h3 className="section-label">{t('my_personal_trail')}</h3>
            {advocacyLogs.length > 0 ? (
              <ListGroup variant="flush">
                {advocacyLogs.map((log) => (
                  <ListGroup.Item key={log.sr_number} className="px-0 py-3 border-light">
                    <div className="d-flex justify-content-between align-items-start">
                      <div>
                        <span className="badge bg-primary-subtle text-primary mb-2 me-2">SR {log.sr_number}</span>
                        <span className={`badge ${log.outcome === 'Pending' ? 'bg-secondary' : 'bg-info'} mb-2`}>{log.outcome}</span>
                        <p className="mb-1 fw-bold small">{log.description || "311 Complaint Filed"}</p>
                        <small className="text-secondary">{new Date(log.created_at).toLocaleString()}</small>
                      </div>
                    </div>
                  </ListGroup.Item>
                ))}
              </ListGroup>
            ) : (
              <Alert variant="light" className="border-dashed py-4 text-center">
                <small className="text-muted fst-italic">{t('no_personal_logs')}</small>
              </Alert>
            )}
          </Col>

          <Col md={6}>
            <h3 className="section-label">{t('community_reports')}</h3>
            <ListGroup variant="flush" className="border rounded bg-light p-2">
              {tenantReports.length > 0 ? (
                tenantReports.slice(0, 5).map((report) => (
                  <ListGroup.Item key={report.id} className="bg-transparent px-2 py-2 border-light small">
                    <Badge bg={report.status === 'UP' ? 'success' : 'danger'} className="me-2">{report.status}</Badge>
                    <span className="text-muted">{new Date(report.reported_at).toLocaleDateString()}</span>
                  </ListGroup.Item>
                ))
              ) : (
                <div className="p-3 text-center small text-muted">{t('no_community_reports')}</div>
              )}
            </ListGroup>
          </Col>

          <Col md={6}>
            <h3 className="section-label">{t('official_history')}</h3>
            <ListGroup variant="flush" className="border rounded bg-light p-2">
              {officialReports.length > 0 ? (
                officialReports.slice(0, 5).map((report, idx) => (
                  <ListGroup.Item key={`official-${report.id || idx}`} className="bg-transparent px-2 py-2 border-light small">
                    <Badge bg="info" className="me-2">DOB</Badge>
                    <span className="text-muted">{new Date(report.reported_at).toLocaleDateString()}</span>
                  </ListGroup.Item>
                ))
              ) : (
                <div className="p-3 text-center small text-muted">{t('no_official_data')}</div>
              )}
            </ListGroup>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
}
