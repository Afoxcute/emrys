import Icon from '@/components/icons';
import { cn } from '@/utils/misc';

interface ModalHeaderProps {
  title: string;
  className?: string;
  onBtnClick?: () => void;
}

export default function ModalHeader({ title, className, onBtnClick }: ModalHeaderProps) {
  return (
    <div className={cn('flex items-center justify-between pb-4', className)}>
      <p className="text-shade-secondary text-base font-medium">{title}</p>
      <div
        onClick={onBtnClick}
        className="text-shade-mute hover:text-shade-primary h-[18px] w-[18px] cursor-pointer"
      >
        <Icon name="Close" />
      </div>
    </div>
  );
}
