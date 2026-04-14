import { Modal } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import { SignupForm } from '../AuthForms';
import type { AuthSuccessData } from '../../types';

interface AuthModalProps {
  show: boolean;
  onHide: () => void;
  onSuccess: (data: AuthSuccessData) => void;
}

export function AuthModal({ show, onHide, onSuccess }: AuthModalProps) {
  const { t } = useTranslation();

  return (
    <Modal
      show={show}
      onHide={onHide}
      centered
      aria-label={t('auth_modal_label')}
    >
      <Modal.Header closeButton className="border-0 pb-0" />
      <Modal.Body className="pt-0">
        <SignupForm onSuccess={onSuccess} />
      </Modal.Body>
    </Modal>
  );
}
