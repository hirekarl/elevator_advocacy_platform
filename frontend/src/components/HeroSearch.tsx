import { Form, Button, Row, Col, Card } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';

interface HeroSearchProps {
  onSearch: (e: React.FormEvent) => void;
  searchData: any;
  setSearchData: (data: any) => void;
  isPending: boolean;
}

export function HeroSearch({ onSearch, searchData, setSearchData, isPending }: HeroSearchProps) {
  const { t } = useTranslation();

  return (
    <div className="py-5 bg-light mb-4 rounded-3 border shadow-sm">
      <div className="container px-4 py-3">
        <h1 className="display-5 fw-bold text-primary mb-3">Resident Action Center</h1>
        <p className="col-md-8 fs-4 text-muted mb-4">
          Enter your address to view your building's elevator service history, DOB complaints, and tenant reports.
        </p>
        
        <Form onSubmit={onSearch} className="p-4 bg-white border rounded shadow-sm">
          <Row className="align-items-end">
            <Col md={2}>
              <Form.Group className="mb-3 mb-md-0">
                <Form.Label className="small fw-bold text-uppercase text-muted">House #</Form.Label>
                <Form.Control
                  type="text"
                  required
                  placeholder="280"
                  size="lg"
                  value={searchData.house_number}
                  onChange={(e) => setSearchData({ ...searchData, house_number: e.target.value })}
                />
              </Form.Group>
            </Col>
            <Col md={5}>
              <Form.Group className="mb-3 mb-md-0">
                <Form.Label className="small fw-bold text-uppercase text-muted">Street Name</Form.Label>
                <Form.Control
                  type="text"
                  required
                  placeholder="Broadway"
                  size="lg"
                  value={searchData.street}
                  onChange={(e) => setSearchData({ ...searchData, street: e.target.value })}
                />
              </Form.Group>
            </Col>
            <Col md={3}>
              <Form.Group className="mb-3 mb-md-0">
                <Form.Label className="small fw-bold text-uppercase text-muted">Borough</Form.Label>
                <Form.Select
                  size="lg"
                  value={searchData.borough}
                  onChange={(e) => setSearchData({ ...searchData, borough: e.target.value })}
                >
                  <option value="Manhattan">Manhattan</option>
                  <option value="Bronx">Bronx</option>
                  <option value="Brooklyn">Brooklyn</option>
                  <option value="Queens">Queens</option>
                  <option value="Staten Island">Staten Island</option>
                </Form.Select>
              </Form.Group>
            </Col>
            <Col md={2}>
              <Button 
                variant="primary" 
                type="submit" 
                className="w-100 py-2 fw-bold"
                size="lg"
                disabled={isPending}
              >
                {isPending ? t('syncing') : 'View Action Center'}
              </Button>
            </Col>
          </Row>
        </Form>
      </div>
    </div>
  );
}
