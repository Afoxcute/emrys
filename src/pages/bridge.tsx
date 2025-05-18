import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { FloatingButtonStrip } from '../components/nav/FloatingButtonStrip';
import { TransferTokenCard } from '../features/transfer/TransferTokenCard';
import TestnetBridge from './testnet-bridge';

const BridgePage: NextPage = () => {
  const router = useRouter();
  const [isTestnet, setIsTestnet] = useState(false);

  useEffect(() => {
    if (router.isReady) {
      setIsTestnet(router.query.network === 'testnet');
    }
  }, [router.isReady, router.query]);

  return (
    <div className="flex min-h-[80vh] flex-col space-y-3 pt-4">
      <div className="jusify-center relative flex-grow items-center">
        {isTestnet ? (
          <TestnetBridge />
        ) : (
          <>
            <TransferTokenCard />
            <FloatingButtonStrip />
          </>
        )}
      </div>
    </div>
  );
};

export default BridgePage;
