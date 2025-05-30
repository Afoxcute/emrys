import Link from 'next/link';

import Image from 'next/image';
import GithubIcon from '../icons/SocialIcons/Github';
import XIcon from '../icons/SocialIcons/X';

export default function Socials() {
  return (
    <div className="flex items-center justify-center gap-12">
      <FooterLogo />
      <div className="text-shade-mute flex items-center justify-center space-x-10 py-10 transition">
        <Link
          href="https://x.com/ProtocolEmrys"
          target="_blank"
          className="hover:text-primary-apollo transition"
        >
          <XIcon />
        </Link>
        <Link
          href="https://github.com/emrys-Org/"
          target="_blank"
          className="hover:text-primary-apollo transition"
        >
          <GithubIcon />
        </Link>
      </div>
    </div>
  );
}

function FooterLogo() {
  return (
    <div className="flex items-center justify-center">
      <div className="ml-2 h-12 w-12 sm:h-14 sm:w-14">
        {/* <HyperlaneLogo color={Color.white} /> */}
      </div>
      <div className="ml-6 space-y-1 text-lg text-white font-medium sm:text-xl">
        <div>Go interchain</div>
        <div className="flex items-center">
          with Emrys
          <Image alt="emrys logo" src="/emrys-logo1.png" width={60} height={80} />
        </div>
      </div>
    </div>
  );
}
