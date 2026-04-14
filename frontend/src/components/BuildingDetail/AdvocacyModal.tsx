import { useTranslation } from 'react-i18next';
import { Modal, Form, Button } from 'react-bootstrap';

interface AdvocacyModalProps {
  show: boolean;
  onHide: () => void;
  formData: { sr_number: string; description: string };
  setFormData: (data: { sr_number: string; description: string }) => void;
  onSubmit: (e: React.FormEvent) => void;
  isSubmitting: boolean;
}

export function AdvocacyModal({
  show,
  onHide,
  formData,
  setFormData,
  onSubmit,
  isSubmitting
}: AdvocacyModalProps) {
  const { t } = useTranslation();

  return (
    <Modal
      show={show}
      onHide={onHide}
      centered
      aria-labelledby="advocacy-modal-title"
    >
      <Modal.Header closeButton className="border-0 pb-0">
        <Modal.Title id="advocacy-modal-title" className="fw-bold">{t('log_311_title')}</Modal.Title>
      </Modal.Header>
      <Modal.Body className="pt-3">
        <p className="text-secondary small mb-4">{t('log_311_help')}</p>
        <Form onSubmit={onSubmit}>
          <Form.Group className="mb-3">
            <Form.Label className="fw-bold small">{t('sr_number_label')}</Form.Label>
            <Form.Control
              type="text"
              placeholder="e.g. 1-1-7654321"
              required
              value={formData.sr_number}
              onChange={(e) => setFormData({ ...formData, sr_number: e.target.value })}
            />
          </Form.Group>
          <Form.Group className="mb-4">
            <Form.Label className="fw-bold small">{t('notes_label')}</Form.Label>
            <Form.Control
              as="textarea"
              rows={2}
              placeholder="e.g. Spoke to operator 42, they said 3 days."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            />
          </Form.Group>
          <Button variant="primary" type="submit" className="w-100 fw-bold py-2" disabled={isSubmitting}>
            {isSubmitting ? t('saving') : t('save_history')}
          </Button>
        </Form>
      </Modal.Body>
    </Modal>
  );
}
