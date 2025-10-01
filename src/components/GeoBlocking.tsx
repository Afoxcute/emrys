import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

const BLOCKED_COUNTRIES = [
  'CU', // Cuban
  'KP', // North Korea
  'RU', // Russia
  'AF', // Afghanistan
  'BY', // Belarus
  'BA', // Bosnia & Herzegovina
  'CF', // Central African Republic
  'CD', // Democratic Republic of the Congo
  'GN', // Guinea
  'GW', // Guinea-Bissau
  'HT', // Haiti
  'IQ', // Iraq
  'LB', // Lebanon
  'LY', // Libya
  'ML', // Mali
  'NI', // Nicaragua
  'SO', // Somalia
  'SS', // South Sudan
  'SD', // Sudan
  'VE', // Venezuela
  'YE', // Yemen
  'ZW', // Zimbabwe
  'MM', // Myanmar
  'SY', // Syria
];

const BLOCKED_REGIONS = [
  {
    country: 'UA', // Ukraine
    regions: [
      '43', // Crimea
      '14', // Donetsk
      '09', // Luhan
    ],
  },
];

export function GeoBlocking({ children }: { children: React.ReactNode }) {
  const [isBlocked, setIsBlocked] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const checkGeoLocation = async () => {
      try {
        // Use a free geolocation service
        const response = await fetch('https://ipapi.co/json/');
        const data = await response.json();
        
        const { country_code, region_code } = data;
        
        if (country_code && BLOCKED_COUNTRIES.includes(country_code)) {
          setIsBlocked(true);
          router.push('/blocked');
          return;
        }
        
        if (
          country_code &&
          region_code &&
          BLOCKED_REGIONS.find((x) => x.country === country_code)?.regions.includes(region_code)
        ) {
          setIsBlocked(true);
          router.push('/blocked');
          return;
        }
      } catch (error) {
        console.warn('Failed to check geolocation:', error);
        // If geolocation fails, allow access
      } finally {
        setIsLoading(false);
      }
    };

    checkGeoLocation();
  }, [router]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (isBlocked) {
    return null;
  }

  return <>{children}</>;
}
