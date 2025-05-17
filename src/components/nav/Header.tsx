import Image from 'next/image';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { ConnectWalletButton } from '../../features/wallet/ConnectWalletButton';

export function Header() {
  const router = useRouter();
  const isHomePage = router.pathname === '/';

  return (
    <header className="w-full px-2 pb-2 pt-3 sm:px-6 lg:px-12">
      <div className="flex items-center justify-between">
        <Link href="/" className="flex items-center py-2 text-xl font-bold text-white">
          <Image alt="emrys logo" src="/emrys-logo1.png" width={60} height={80} />
        </Link>

        <div className="flex items-center gap-4">
          {!isHomePage && (
            <Link
              href="/"
              className="hidden rounded-lg px-4 py-2 text-sm font-medium text-white transition-all hover:bg-white/10 sm:block"
            >
              Home
            </Link>
          )}

          <Link
            href="/bridge"
            className="hidden rounded-lg px-4 py-2 text-sm font-medium text-white transition-all hover:bg-white/10 sm:block"
          >
            Bridge
          </Link>

          <ConnectWalletButton />
        </div>
      </div>
    </header>
  );
}
