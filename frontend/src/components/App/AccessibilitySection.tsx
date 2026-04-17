import { useTranslation } from 'react-i18next';

export function AccessibilitySection() {
  const { t } = useTranslation();

  return (
    <section className="ac-section" aria-label="Accessibility commitment">
      <div className="container">
        {/* Section header */}
        <div className="mb-5">
          <span className="ac-section-label d-block mb-2">{t('ac_label')}</span>
          <h2 className="ac-heading mb-2">{t('ac_heading')}</h2>
          <p className="ac-subheading">{t('ac_subheading')}</p>
        </div>

        <div className="row g-4 align-items-start">
          {/* Martha card — col-md-5 */}
          <div className="col-12 col-md-5">
            <div className="ac-martha-card">
              <div className="ac-martha-label">{t('ac_martha_label')}</div>
              <div className="ac-martha-name">{t('ac_martha_name')}</div>
              <div className="ac-martha-context">{t('ac_martha_context')}</div>
              <ul className="ac-martha-jobs" aria-label="Martha's three jobs">
                <li>{t('ac_martha_job1')}</li>
                <li>{t('ac_martha_job2')}</li>
                <li>{t('ac_martha_job3')}</li>
              </ul>
              <p className="ac-martha-note">{t('ac_martha_note')}</p>
            </div>
          </div>

          {/* Lighthouse CI scores — col-md-4 */}
          <div className="col-12 col-md-4">
            <div className="ac-scores-card">
              <div className="ac-scores-label">{t('ac_scores_label')}</div>

              <div className="ac-score-item">
                <span className="ac-score-num" aria-label="93 out of 100">93</span>
                <span className="ac-score-denom" aria-hidden="true">/100</span>
                <span className="ac-score-desc">{t('ac_score_home_label')}</span>
              </div>

              <div className="ac-score-item ac-score-item--perfect">
                <span className="ac-score-num" aria-label="100 out of 100">100</span>
                <span className="ac-score-denom" aria-hidden="true">/100</span>
                <span className="ac-score-desc">{t('ac_score_data_label')}</span>
              </div>

              <div className="ac-score-item ac-score-item--perfect">
                <span className="ac-score-num" aria-label="100 out of 100">100</span>
                <span className="ac-score-denom" aria-hidden="true">/100</span>
                <span className="ac-score-desc">{t('ac_score_seo_label')}</span>
              </div>

              <p className="ac-scores-note">{t('ac_scores_note')}</p>
            </div>
          </div>

          {/* Methods — col-md-3 */}
          <div className="col-12 col-md-3">
            <div className="ac-methods-card">
              <div className="ac-methods-label">{t('ac_methods_label')}</div>
              <ul className="ac-methods-list" aria-label="Verification methods">
                <li>
                  <span className="ac-method-check" aria-hidden="true">✓</span>
                  {t('ac_method_playwright')}
                </li>
                <li>
                  <span className="ac-method-check" aria-hidden="true">✓</span>
                  {t('ac_method_axe')}
                </li>
                <li>
                  <span className="ac-method-check" aria-hidden="true">✓</span>
                  {t('ac_method_lhci')}
                </li>
                <li>
                  <span className="ac-method-check" aria-hidden="true">✓</span>
                  {t('ac_method_wcag')}
                </li>
              </ul>
              <div className="ac-test-count">
                <div className="ac-test-num" aria-label="6 Martha journey tests">6</div>
                <div className="ac-test-label">{t('ac_test_count_label')}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
