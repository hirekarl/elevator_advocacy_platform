import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import type { AuthSuccessData } from '../types';

export function useAuth() {
  const navigate = useNavigate();
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem('token'));
  const [username, setUsername] = useState(localStorage.getItem('username') || '');
  const [primaryBuildingBin, setPrimaryBuildingBin] = useState<string | null>(localStorage.getItem('primary_building_bin'));
  const [showAuthModal, setShowAuthModal] = useState(false);

  const [showGuide, setShowGuide] = useState(false);

  const handleLogout = useCallback(() => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('primary_building_bin');
    setIsLoggedIn(false);
    setUsername('');
    setPrimaryBuildingBin(null);
    navigate('/');
  }, [navigate]);

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await fetch('http://localhost:8000/api/auth/whoami/', {
            headers: { 'Authorization': `Token ${token}` }
          });
          if (response.ok) {
            const data = await response.json();
            setIsLoggedIn(true);
            setUsername(data.username);

            if (data.primary_building) {
              const currentBinInStorage = localStorage.getItem('primary_building_bin');
              if (currentBinInStorage !== data.primary_building.bin) {
                localStorage.setItem('primary_building_bin', data.primary_building.bin);
              }
              setPrimaryBuildingBin(data.primary_building.bin);
            } else {
              setPrimaryBuildingBin(null);
            }
          } else if (response.status === 401) {
            handleLogout();
          }
        } catch (error) {
          console.error("Auth sync error:", error);
        }
      }
    };

    fetchUser();
  }, [handleLogout]);

  const handleAuthSuccess = (data: AuthSuccessData) => {
    setIsLoggedIn(true);
    setUsername(data.username);
    setShowAuthModal(false);
    if (data.primary_building) {
      localStorage.setItem('primary_building_bin', data.primary_building.bin);
      setPrimaryBuildingBin(data.primary_building.bin);
      navigate(`/building/${data.primary_building.bin}`);
    }
  };

  return {
    isLoggedIn,
    setIsLoggedIn,
    username,
    setUsername,
    primaryBuildingBin,
    setPrimaryBuildingBin,
    showAuthModal,
    setShowAuthModal,
    showGuide,
    setShowGuide,
    handleLogout,
    handleAuthSuccess
  };
}
