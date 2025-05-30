import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useState } from 'react';
import { SolidButton } from '../components/buttons/SolidButton';
import FaqChat from '../components/faq/FaqChat';
import { APP_DESCRIPTION, APP_NAME } from '../consts/app';

const Home: NextPage = () => {
  const router = useRouter();
  const [showDropdown, setShowDropdown] = useState(false);

  const handleStartBridging = () => {
    setShowDropdown(!showDropdown);
  };

  const navigateToBridge = (network: string) => {
    if (network === 'utxo') {
      router.push('/utxo');
    }

    if (network === 'mainnet') {
      router.push('/bridge');
    } else {
      // For testnet, you can define a different route if needed
      router.push('/bridge?network=testnet');
    }
    setShowDropdown(false);
  };

  return (
    <div className="flex flex-col items-center justify-center px-6 py-10 text-center">
      <div className="max-w-3xl">
        <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl md:text-6xl">
          {APP_NAME}
        </h1>

        <p className="mt-6 text-xl text-white/90 sm:text-2xl">{APP_DESCRIPTION}</p>

        <div className="mt-8 max-w-2xl">
          <p className="mb-6 text-lg text-white/80">
            Emrys is a powerful cross-chain bridge powered by our own forked version of SVM & IBC
            implementation. Seamlessly transfer tokens between different blockchains with minimal
            fees and maximum security.
          </p>

          <ul className="mb-8 list-inside list-disc space-y-2 text-left text-white/80">
            <li>Fast, secure transfers between multiple chains</li>
            <li>Support for native tokens and popular standards</li>
            <li>Simple, user-friendly interface</li>
            <li>Powered by our own forked version of SVM & IBC implementation</li>
          </ul>
        </div>

        <div className="relative mt-10">
          <SolidButton
            onClick={handleStartBridging}
            className="px-8 py-3 text-lg font-medium transition-all duration-300 hover:scale-105"
            color="accent"
          >
            Start Bridging
          </SolidButton>

          {showDropdown && (
            <div className="absolute z-10 mt-2 w-full overflow-hidden rounded-md bg-primary-600 shadow-lg">
              <div className="py-1">
                <button
                  onClick={() => navigateToBridge('mainnet')}
                  className="block w-full px-4 py-2 text-left text-sm text-white"
                >
                  Bridge on Mainnet
                </button>
                <button
                  onClick={() => navigateToBridge('testnet')}
                  className="block w-full px-4 py-2 text-left text-sm text-white"
                >
                  Bridge on Testnet
                </button>
                <button
                  onClick={() => navigateToBridge('utxo')}
                  className="block w-full px-4 py-2 text-left text-sm text-white"
                >
                  ZPL UTXO Bridge
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Walrus Decentralized Storage Section */}
      <div className="mt-16 w-full max-w-3xl">
        <div className="rounded-lg bg-white/10 p-6 shadow-lg backdrop-blur-sm">
          <h2 className="mb-3 text-2xl font-bold text-white">
            Powered by Walrus Decentralized Storage
          </h2>
          <p className="mb-4 text-white/80">
            Emrys integrates with Walrus, a next-generation decentralized storage solution that
            ensures your transaction data remains secure, immutable, and accessible across multiple
            networks.
          </p>
          <div className="grid grid-cols-1 gap-4 text-white/90 md:grid-cols-3">
            <div className="rounded-lg bg-primary-600/40 p-4">
              <h3 className="mb-2 font-semibold">Secure Storage</h3>
              <p className="text-sm">
                Your cross-chain transaction data is encrypted and stored across a distributed
                network.
              </p>
            </div>
            <div className="rounded-lg bg-primary-600/40 p-4">
              <h3 className="mb-2 font-semibold">Data Permanence</h3>
              <p className="text-sm">
                Never lose access to your transaction history with permanent on-chain storage.
              </p>
            </div>
            <div className="rounded-lg bg-primary-600/40 p-4">
              <h3 className="mb-2 font-semibold">Rapid Retrieval</h3>
              <p className="text-sm">
                Access your data instantly across any supported blockchain network.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-16 w-full pb-10">
        <h2 className="mb-6 text-2xl font-bold text-white">Have Questions? Ask Our AI Assistant</h2>
        <p className="mb-6 text-white/80">
          Powered by <span className="font-semibold">fetch.ai uAgents</span> - Our intelligent
          assistant can answer all your questions about Emrys.
        </p>
        <FaqChat />
      </div>
    </div>
  );
};

export default Home;
