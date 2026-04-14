import { useState, useTransition, useCallback, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import type { Building } from '../types';
import { API_BASE } from '../utils/api';

export function useBuildingLookup(primaryBuildingBin: string | null) {
  const { bin } = useParams();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [isPending, startTransition] = useTransition();
  const [activeBuilding, setActiveBuilding] = useState<Building | null>(null);
  const [buildingNotFound, setBuildingNotFound] = useState(false);
  const [searchError, setSearchError] = useState('');
  const [searchData, setSearchData] = useState({
    house_number: '',
    street: '',
    borough: 'Manhattan'
  });
  const [primaryBuildingStatus, setPrimaryBuildingStatus] = useState<string | null>(null);

  const fetchBuilding = useCallback((binId: string) => {
    setBuildingNotFound(false);
    startTransition(async () => {
      try {
        const response = await fetch(`${API_BASE}/api/buildings/${binId}/`);
        if (response.ok) {
          const data = await response.json();
          setActiveBuilding(data);
        } else {
          setActiveBuilding(null);
          setBuildingNotFound(true);
        }
      } catch (error) {
        console.error("Fetch Error:", error);
      }
    });
  }, []);

  useEffect(() => {
    if (bin) {
      fetchBuilding(bin);
    } else {
      setActiveBuilding(null);
    }
  }, [bin, fetchBuilding]);

  useEffect(() => {
    if (primaryBuildingBin && !bin) {
      fetch(`${API_BASE}/api/buildings/${primaryBuildingBin}/`)
        .then(res => res.ok ? res.json() : null)
        .then(data => { if (data) setPrimaryBuildingStatus(data.verified_status ?? null); })
        .catch(() => {});
    } else {
      setPrimaryBuildingStatus(null);
    }
  }, [primaryBuildingBin, bin]);

  const handleSearch = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setSearchError('');

    startTransition(async () => {
      try {
        const { house_number, street, borough } = searchData;
        if (!house_number || !street) return;
        const query = new URLSearchParams({ house_number, street, borough }).toString();
        const response = await fetch(`${API_BASE}/api/buildings/lookup/?${query}`);

        if (response.ok) {
          const data = await response.json();
          navigate(`/building/${data.bin}`);
        } else {
          setSearchError(t('building_not_found'));
        }
      } catch (error) {
        console.error("Search Error:", error);
        setSearchError(t('building_not_found'));
      }
    });
  };

  return {
    bin,
    isPending,
    activeBuilding,
    buildingNotFound,
    searchError,
    searchData,
    setSearchData,
    primaryBuildingStatus,
    handleSearch,
    fetchBuilding
  };
}
