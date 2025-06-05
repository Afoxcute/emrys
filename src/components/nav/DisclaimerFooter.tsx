
export function DisclaimerFooter() {
  return (
    <div className="w-full bg-primary-700/70 backdrop-blur-sm py-3 px-4 mt-auto">
      <div className="max-w-6xl mx-auto text-center">
        <p className="text-white/90 text-xs font-medium tracking-wide uppercase">
          DISCLAIMER: Emrys uses SVM & IBC & WALRUS for secure transactions & speed
        </p>
        <p className="text-white/70 text-xs mt-1">
          All transactions are processed using our proprietary implementation of SVM (Solana Virtual Machine) and IBC (Inter-Blockchain Communication) protocols, with data secured through Walrus decentralized storage
        </p>
      </div>
    </div>
  );
} 