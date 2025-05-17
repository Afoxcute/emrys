import { useEffect, useState } from 'react';
import { toast } from 'react-toastify';
import { SolidButton } from '../components/buttons/SolidButton';
import { Card } from '../components/layout/Card';
import { DisclaimerFooter } from '../components/nav/DisclaimerFooter';
import { logger } from '../utils/logger';

// Chain configuration with native token information
const chainConfigs = {
  'Ethereum': {
    nativeToken: 'ETH',
    tokenSymbol: 'ETH',
    decimals: 18,
    icon: '⟠'
  },
  'Avalanche': {
    nativeToken: 'AVAX',
    tokenSymbol: 'AVAX',
    decimals: 18,
    icon: '🔺'
  },
  'Polygon': {
    nativeToken: 'MATIC',
    tokenSymbol: 'MATIC',
    decimals: 18,
    icon: '⬡'
  },
  'BSC': {
    nativeToken: 'BNB',
    tokenSymbol: 'BNB',
    decimals: 18,
    icon: '💛'
  }
};

export default function TestnetBridge() {
  const [amount, setAmount] = useState('');
  const [recipientAddress, setRecipientAddress] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState('');
  const [sourceChain, setSourceChain] = useState('Avalanche');
  
  // List of available EVM chains for source
  const sourceChains = Object.keys(chainConfigs);
  
  // Display the current step of the bridging process
  useEffect(() => {
    if (currentStep) {
      toast.info(currentStep);
    }
  }, [currentStep]);

  const handleBridge = async () => {
    if (!amount || parseFloat(amount) <= 0) {
      toast.error('Please enter a valid amount');
      return;
    }

    if (!recipientAddress) {
      toast.error('Please enter a recipient address');
      return;
    }
    
    setIsLoading(true);
    
    try {
      const nativeToken = chainConfigs[sourceChain].nativeToken;
      
      // In a real implementation, this would use the Emrys SDK
      // For demo purposes, we'll simulate the steps
      setCurrentStep('Initializing Emrys cross-chain messaging');
      await simulateDelay(1000);
      
      setCurrentStep(`Preparing ${nativeToken} to SOL transfer`);
      await simulateDelay(1500);
      
      setCurrentStep('Getting transfer quote');
      await simulateDelay(1500);
      
      setCurrentStep(`Initiating transfer from ${sourceChain}`);
      await simulateDelay(2000);
      
      setCurrentStep('Waiting for transaction confirmation');
      await simulateDelay(3000);
      
      setCurrentStep('Getting attestation');
      await simulateDelay(2000);
      
      setCurrentStep('Completing transfer to Solana');
      await simulateDelay(2500);
      
      // Success!
      toast.success(`Transfer completed! ${amount} ${nativeToken} has been bridged to SOL on Solana`);
      
      // Reset form
      setAmount('');
      setRecipientAddress('');
      setCurrentStep('');
    } catch (error) {
      logger.error('Bridge error:', error);
      toast.error('An error occurred during the bridging process');
    } finally {
      setIsLoading(false);
    }
  };
  
  const simulateDelay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

  const getCurrentNativeToken = () => {
    return chainConfigs[sourceChain].nativeToken;
  };

  return (
    <>
      <Card className="w-100 sm:w-[31rem]">
        <div className="flex flex-col p-2">
          <h1 className="mb-4 text-2xl font-bold text-primary-500">Emrys Testnet Bridge</h1>
          <p className="mb-6 text-sm text-gray-600">Bridge native tokens from EVM chains to SOL on Solana using Emrys</p>
          
          <div className="mb-4">
            <label className="block pl-0.5 text-sm text-gray-600">Source Chain</label>
            <div className="mt-1.5 flex rounded-lg border border-primary-300">
              <select 
                value={sourceChain}
                onChange={(e) => setSourceChain(e.target.value)}
                className="w-full rounded-lg border-none bg-transparent px-2.5 py-2.5 text-sm outline-none"
                disabled={isLoading}
              >
                {sourceChains.map(chain => (
                  <option key={chain} value={chain}>{chain}</option>
                ))}
              </select>
            </div>
          </div>
          
          <div className="mb-4">
            <label className="block pl-0.5 text-sm text-gray-600">Destination Chain</label>
            <div className="mt-1.5 flex rounded-lg border border-primary-300 bg-gray-100">
              <input 
                type="text" 
                value="Solana" 
                className="w-full rounded-lg border-none bg-transparent px-2.5 py-2.5 text-sm outline-none"
                disabled={true}
              />
            </div>
          </div>
          
          <div className="mb-4">
            <label className="block pl-0.5 text-sm text-gray-600">Token</label>
            <div className="mt-1.5 flex items-center rounded-lg border border-primary-300 px-2.5 py-2.5">
              <div className="mr-2">{chainConfigs[sourceChain].icon}</div>
              <div className="flex-1 font-medium text-gray-700">
                {getCurrentNativeToken()} <span className="text-xs text-gray-500">(Native)</span>
              </div>
              <div className="text-xs text-gray-500">to</div>
              <div className="ml-2 font-medium text-gray-700">SOL</div>
            </div>
          </div>
          
          <div className="mb-4">
            <label className="block pl-0.5 text-sm text-gray-600">Amount</label>
            <div className="relative mt-1.5">
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="0.00"
                className="w-full rounded-lg border border-primary-300 px-2.5 py-2.5 text-sm outline-none focus:border-primary-500"
                disabled={isLoading}
              />
              <div className="absolute inset-y-0 right-0 flex items-center px-3 pointer-events-none text-gray-500">
                {getCurrentNativeToken()}
              </div>
            </div>
          </div>
          
          <div className="mb-6">
            <label className="block pl-0.5 text-sm text-gray-600">Recipient Solana Address</label>
            <div className="relative mt-1.5">
              <input
                type="text"
                value={recipientAddress}
                onChange={(e) => setRecipientAddress(e.target.value)}
                placeholder="Solana address or wallet"
                className="w-full rounded-lg border border-primary-300 px-2.5 py-2.5 text-sm outline-none focus:border-primary-500"
                disabled={isLoading}
              />
            </div>
          </div>
          
          <SolidButton
            onClick={handleBridge}
            disabled={isLoading}
            color="accent"
            className="py-3"
          >
            {isLoading ? (
              <div className="flex items-center justify-center">
                <div className="h-5 w-5 animate-spin rounded-full border-b-2 border-white"></div>
                <span className="ml-2">Processing...</span>
              </div>
            ) : (
              `Bridge ${getCurrentNativeToken()} to SOL`
            )}
          </SolidButton>
          
          <div className="mt-4 rounded-lg bg-gray-100 p-4 text-xs text-gray-600">
            <p className="font-medium">⚠️ Testnet Only</p>
            <p className="mt-1">This bridge uses Emrys protocol on testnet. Tokens sent are not real assets.</p>
          </div>
        </div>
      </Card>
      
      <div className="w-full max-w-[31rem] mt-4">
        <DisclaimerFooter />
      </div>
    </>
  );
} 