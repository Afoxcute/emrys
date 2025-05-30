import GlobalModals from '@/components/GlobalModals/GlobalModals';
import { BitcoinWalletProvider } from '@/contexts/BitcoinWalletProvider';
import SolanaWalletProvider from '@/contexts/SolanaWalletProvider';
import { ZplClientProvider } from '@/contexts/ZplClientProvider';
import { useIsSsr } from '@hyperlane-xyz/widgets';
import '@hyperlane-xyz/widgets/styles.css';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Analytics } from '@vercel/analytics/react';
import type { AppProps } from 'next/app';
import { useRouter } from 'next/router';
import { ToastContainer, Zoom } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { ErrorBoundary } from '../components/errors/ErrorBoundary';
import { AppLayout } from '../components/layout/AppLayout';
import { UtxoLayout } from '../components/layout/UtxoLayout';
import { MAIN_FONT } from '../consts/app';
import { WarpContextInitGate } from '../features/WarpContextInitGate';
import { CosmosWalletContext } from '../features/wallet/context/CosmosWalletContext';
import { EvmWalletContext } from '../features/wallet/context/EvmWalletContext';
import { SolanaWalletContext } from '../features/wallet/context/SolanaWalletContext';
import { StarknetWalletContext } from '../features/wallet/context/StarknetWalletContext';
import '../styles/aglobals.scss';
import '../styles/design-system.css';
import '../styles/globals.css';
import '../vendor/inpage-metamask';
import '../vendor/polyfill';

const reactQueryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
    },
  },
});

export default function App({ Component, pageProps }: AppProps) {
  // Disable app SSR for now as it's not needed and
  // complicates wallet and graphql integrations
  const isSsr = useIsSsr();
  if (isSsr) {
    return <div></div>;
  }

  const router = useRouter();
  const path = router.pathname;

  const isUtxoRoute = path.startsWith('/utxo');

  const Layout = isUtxoRoute ? UtxoLayout : AppLayout;

  // Note, the font definition is required both here and in _document.tsx
  // Otherwise Next.js will not load the font
  return (
    <div className={`${MAIN_FONT.variable} font-sans text-black`}>
      <ErrorBoundary>
        <SolanaWalletProvider>
          <ZplClientProvider>
            <BitcoinWalletProvider>
              <GlobalModals />
              <QueryClientProvider client={reactQueryClient}>
                <WarpContextInitGate>
                  <EvmWalletContext>
                    <SolanaWalletContext>
                      <CosmosWalletContext>
                        <StarknetWalletContext>
                          <Layout>
                            <Component {...pageProps} />
                            <Analytics />
                          </Layout>
                        </StarknetWalletContext>
                      </CosmosWalletContext>
                    </SolanaWalletContext>
                  </EvmWalletContext>
                </WarpContextInitGate>
              </QueryClientProvider>
            </BitcoinWalletProvider>
          </ZplClientProvider>
        </SolanaWalletProvider>
        <ToastContainer transition={Zoom} position="bottom-right" limit={2} />
      </ErrorBoundary>
    </div>
  );
}
