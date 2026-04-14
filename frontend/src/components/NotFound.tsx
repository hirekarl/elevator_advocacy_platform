import { Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

export function NotFound() {
  const { t } = useTranslation();

  return (
    <Container
      className="d-flex flex-column align-items-center justify-content-center min-vh-100 text-center"
      style={{ color: 'var(--c-text)' }}
    >
      <p
        className="fw-bold mb-2"
        style={{ fontSize: '4rem', lineHeight: 1, color: 'var(--c-navy)' }}
        aria-hidden="true"
      >
        404
      </p>
      <h1 className="h3 mb-3" style={{ color: 'var(--c-navy)' }}>
        {t('page_not_found_title')}
      </h1>
      <p className="mb-4" style={{ color: 'var(--c-muted)', maxWidth: '24rem' }}>
        {t('page_not_found_message')}
      </p>
      <Link to="/" className="btn btn-primary">
        {t('search_again')}
      </Link>
    </Container>
  );
}
