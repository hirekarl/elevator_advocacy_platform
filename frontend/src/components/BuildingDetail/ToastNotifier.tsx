import { Toast, ToastContainer } from 'react-bootstrap';

interface ToastNotifierProps {
  show: boolean;
  onClose: () => void;
  message: string;
  variant: string;
}

export function ToastNotifier({ show, onClose, message, variant }: ToastNotifierProps) {
  return (
    <ToastContainer position="top-end" className="p-3" style={{ zIndex: 9999 }}>
      <Toast
        onClose={onClose}
        show={show}
        delay={3000}
        autohide
        bg={variant}
        className={variant === 'light' ? 'text-dark' : 'text-white'}
        aria-live={variant === 'danger' || variant === 'warning' ? 'assertive' : 'polite'}
        aria-atomic="true"
      >
        <Toast.Body className="fw-medium">{message}</Toast.Body>
      </Toast>
    </ToastContainer>
  );
}
