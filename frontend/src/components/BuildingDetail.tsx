import { useState } from 'react';
import { Card, ProgressBar, ListGroup, Badge, Alert } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';

interface BuildingDetailProps {
  buildingData: any;
}

export function BuildingDetail({ buildingData }: BuildingDetailProps) {
  const { t } = useTranslation();

  if (!buildingData) return null;

  return (
    <Card className="mt-4 shadow-sm">
      <Card.Header className="bg-primary text-white d-flex justify-content-between align-items-center">
        <h2 className="mb-0">{buildingData.address}</h2>
        <Badge bg="light" text="dark">BIN: {buildingData.bin}</Badge>
      </Card.Header>
      <Card.Body>
        <div className="mb-4">
          <h5 className="text-muted">{t('borough')}</h5>
          <p className="lead">{buildingData.borough}</p>
        </div>

        <div className="mb-4">
          <h5>{t('loss_of_service')}</h5>
          <ProgressBar 
            now={buildingData.loss_of_service_30d} 
            label={`${buildingData.loss_of_service_30d}%`} 
            variant={buildingData.loss_of_service_30d > 10 ? 'danger' : 'warning'}
            className="mb-2"
            style={{ height: '30px' }}
          />
          <small className="text-muted">
            {t('verified_status')}: <strong>{buildingData.verified_status}</strong>
          </small>
        </div>

        <div className="mb-4 bg-light p-3 rounded border">
          <h5 className="d-flex justify-content-between align-items-center">
            7-Day Maintenance Forecast
            <Badge bg={buildingData.failure_risk?.risk_score > 60 ? 'danger' : buildingData.failure_risk?.risk_score > 30 ? 'warning' : 'success'}>
              {buildingData.failure_risk?.risk_score}% Risk
            </Badge>
          </h5>
          <p className="small text-muted mb-2">
            Estimated likelihood of service interruption based on historical activity and recent reports.
          </p>
          <div className="d-flex align-items-center">
            <span className="me-2 small text-uppercase fw-bold">Data Reliability:</span>
            <ProgressBar 
              now={buildingData.failure_risk?.confidence} 
              variant="info" 
              style={{ height: '8px', width: '80px' }} 
            />
            <span className="ms-2 small text-muted">{buildingData.failure_risk?.confidence}%</span>
          </div>
        </div>

        <hr />

        <h5>{t('recent_activity')}</h5>
        <ListGroup variant="flush">
          {buildingData.recent_reports?.length > 0 ? (
            buildingData.recent_reports.map((report: any, idx: number) => (
              <ListGroup.Item key={idx} className="d-flex justify-content-between align-items-center">
                <div>
                  <Badge bg={report.status === 'UP' ? 'success' : 'danger'} className="me-2">
                    {report.status}
                  </Badge>
                  {new Date(report.reported_at).toLocaleString()}
                </div>
                {report.is_official && <Badge bg="info">NYC SODA</Badge>}
              </ListGroup.Item>
            ))
          ) : (
            <Alert variant="light">{t('no_outages')}</Alert>
          )}
        </ListGroup>
      </Card.Body>
    </Card>
  );
}
