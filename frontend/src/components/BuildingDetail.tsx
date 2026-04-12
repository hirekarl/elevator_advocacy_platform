import { Card, ProgressBar, ListGroup, Badge, Alert, Row, Col } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';

interface BuildingDetailProps {
  buildingData: any;
}

export function BuildingDetail({ buildingData }: BuildingDetailProps) {
  const { t } = useTranslation();

  if (!buildingData) return null;

  const tenantReports = buildingData.recent_reports?.filter((r: any) => !r.is_official) || [];
  const officialReports = buildingData.recent_reports?.filter((r: any) => r.is_official) || [];

  return (
    <div className="building-action-center">
      <Card className="border-0 shadow-sm mb-4">
        <Card.Body className="p-4">
          <div className="d-flex justify-content-between align-items-start mb-3">
            <div>
              <h2 className="fw-bold mb-1 text-primary">{buildingData.address}</h2>
              <p className="text-muted mb-0">{buildingData.borough} • BIN {buildingData.bin}</p>
            </div>
            <Badge bg={buildingData.verified_status === 'DOWN' ? 'danger' : 'success'} className="px-3 py-2 fs-6">
              Status: {buildingData.verified_status}
            </Badge>
          </div>

          <Row className="g-4 mt-2">
            <Col md={6}>
              <div className="p-3 bg-light rounded border">
                <h6 className="text-uppercase fw-bold text-muted small mb-3">Service Reliability</h6>
                <div className="d-flex align-items-end mb-2">
                  <span className="display-6 fw-bold me-2">{100 - buildingData.loss_of_service_30d}%</span>
                  <span className="text-muted mb-1 pb-1">Uptime (30d)</span>
                </div>
                <ProgressBar 
                  now={100 - buildingData.loss_of_service_30d} 
                  variant={buildingData.loss_of_service_30d > 10 ? 'warning' : 'success'}
                  style={{ height: '8px' }}
                />
              </div>
            </Col>
            <Col md={6}>
              <div className="p-3 bg-light rounded border">
                <h6 className="text-uppercase fw-bold text-muted small mb-3">Maintenance Forecast</h6>
                <div className="d-flex align-items-end mb-2">
                  <span className="display-6 fw-bold me-2">{buildingData.failure_risk?.risk_score}%</span>
                  <span className="text-muted mb-1 pb-1">Risk Level</span>
                </div>
                <ProgressBar 
                  now={buildingData.failure_risk?.risk_score} 
                  variant={buildingData.failure_risk?.risk_score > 60 ? 'danger' : 'warning'}
                  style={{ height: '8px' }}
                />
              </div>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      <h4 className="fw-bold mb-4 mt-5">Historical Action Timeline</h4>
      
      <Row>
        <Col md={6}>
          <Card className="h-100 border-0 shadow-sm">
            <Card.Header className="bg-white border-0 pt-4 px-4">
              <h5 className="fw-bold mb-0">Tenant Community Reports</h5>
              <p className="small text-muted">Real-time issues reported by your neighbors.</p>
            </Card.Header>
            <Card.Body className="px-4 pb-4">
              <ListGroup variant="flush">
                {tenantReports.length > 0 ? (
                  tenantReports.map((report: any, idx: number) => (
                    <ListGroup.Item key={idx} className="px-0 py-3 border-light">
                      <div className="d-flex justify-content-between">
                        <Badge bg={report.status === 'UP' ? 'success-subtle' : 'danger-subtle'} className={`text-${report.status === 'UP' ? 'success' : 'danger'} mb-2`}>
                          {report.status}
                        </Badge>
                        <small className="text-muted">{new Date(report.reported_at).toLocaleDateString()}</small>
                      </div>
                      <p className="mb-0 small fw-medium">User reported elevator as {report.status.toLowerCase()}.</p>
                    </ListGroup.Item>
                  ))
                ) : (
                  <Alert variant="light" className="border-dashed py-4 text-center">No community reports logged.</Alert>
                )}
              </ListGroup>
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card className="h-100 border-0 shadow-sm">
            <Card.Header className="bg-white border-0 pt-4 px-4">
              <h5 className="fw-bold mb-0">Official DOB History</h5>
              <p className="small text-muted">Official complaints synced from NYC Open Data.</p>
            </Card.Header>
            <Card.Body className="px-4 pb-4">
              <ListGroup variant="flush">
                {officialReports.length > 0 ? (
                  officialReports.map((report: any, idx: number) => (
                    <ListGroup.Item key={idx} className="px-0 py-3 border-light">
                      <div className="d-flex justify-content-between">
                        <Badge bg="info-subtle" className="text-info mb-2">DOB COMPLAINT</Badge>
                        <small className="text-muted">{new Date(report.reported_at).toLocaleDateString()}</small>
                      </div>
                      <p className="mb-0 small fw-medium">Official record of elevator inoperative.</p>
                    </ListGroup.Item>
                  ))
                ) : (
                  <Alert variant="light" className="border-dashed py-4 text-center">No official DOB complaints found.</Alert>
                )}
              </ListGroup>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
}
