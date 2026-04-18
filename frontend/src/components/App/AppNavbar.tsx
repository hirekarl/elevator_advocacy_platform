import { Navbar, Container, Button, Dropdown, Alert } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

const LANGUAGES = [
  { code: 'en', label: 'English',           short: 'EN'  },
  { code: 'es', label: 'Español / Spanish', short: 'ES'  },
  { code: 'zh', label: '中文 / Mandarin',   short: '中文' },
  { code: 'bn', label: 'বাংলা / Bengali',   short: 'বাং' },
] as const;

interface AppNavbarProps {
  isLoggedIn: boolean;
  username: string;
  onLogout: () => void;
  onShowAuthModal: () => void;
  onShowGuide: () => void;
  changeLanguage: (lang: string) => void;
}

export function AppNavbar({
  isLoggedIn,
  username,
  onLogout,
  onShowAuthModal,
  onShowGuide,
  changeLanguage
}: AppNavbarProps) {
  const { t, i18n } = useTranslation();

  const isNonEnglish = i18n.language !== 'en';
  const currentLang = LANGUAGES.find(l => l.code === i18n.language) ?? LANGUAGES[0];

  return (
    <>
      <Navbar
        variant="dark"
        expand="lg"
        className="shadow-sm sticky-top py-2 py-lg-3 app-navbar"
        aria-label={t('guide_modal_label')}
      >
        <Container>
          <Navbar.Brand as={Link} to="/" className="d-flex align-items-center gap-2">
            <span className="brand-mark" aria-hidden="true">▲</span>
            ELEVATOR ADVOCATE
          </Navbar.Brand>
          <div className="d-flex align-items-center ms-auto">
            <Link to="/data" className="ds-nav-link me-2 me-md-3 fs-7">
              {t('nav_data')}
            </Link>
            <Button
              variant="link"
              className="text-info text-decoration-none fw-bold me-2 me-md-3 p-0 fs-7 fs-md-6"
              onClick={onShowGuide}
            >
              <span aria-hidden="true">❓</span> {t('how_to_use')}
            </Button>

            <Dropdown align="end" className="me-2 me-md-3">
              <Dropdown.Toggle
                variant="outline-light"
                size="sm"
                className="border-0 fw-bold lang-toggle"
                aria-label={t('toggle_language')}
              >
                <span aria-hidden="true">🌐</span>{' '}
                <span lang={currentLang.code}>{currentLang.short}</span>
              </Dropdown.Toggle>
              <Dropdown.Menu>
                {LANGUAGES.map(({ code, label }) => (
                  <Dropdown.Item
                    key={code}
                    lang={code}
                    onClick={() => changeLanguage(code)}
                    active={i18n.language === code}
                    aria-current={i18n.language === code ? true : undefined}
                  >
                    {label}
                  </Dropdown.Item>
                ))}
              </Dropdown.Menu>
            </Dropdown>

            {isLoggedIn ? (
              <Dropdown align="end">
                <Dropdown.Toggle
                  variant="outline-info"
                  size="sm"
                  className="fw-bold px-3"
                >
                  <span className="d-none d-md-inline">{username}</span>
                  <span className="d-md-none" aria-hidden="true">👤</span>
                </Dropdown.Toggle>
                <Dropdown.Menu>
                  <Dropdown.Item onClick={onLogout}>{t('log_out')}</Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            ) : (
              <Button
                variant="primary"
                size="sm"
                className="fw-bold px-3 rounded-pill"
                onClick={onShowAuthModal}
              >
                {t('login_button')}
              </Button>
            )}
          </div>
        </Container>
      </Navbar>
      {isNonEnglish && (
        <Alert
          variant="warning"
          className="rounded-0 py-1 px-3 mb-0 text-center small border-0"
        >
          Translations are machine-generated and may contain errors.
        </Alert>
      )}
    </>
  );
}
