import type { Asset } from '../types/asset';
import { formatCurrency } from '../utils/format';

interface AssetItemProps {
  asset: Asset;
}

export function AssetItem({ asset }: AssetItemProps) {
  const displayName = asset.nickname || asset.asset_name || 'Unnamed Asset';
  
  return (
    <div className="flex items-center justify-between py-3 px-4 bg-white border-b border-slate-100 last:border-b-0 hover:bg-slate-50 transition-colors">
      <div>
        <p className="text-sm font-medium text-slate-700">{displayName}</p>
        {asset.institution_name && (
          <p className="text-xs text-slate-500">{asset.institution_name}</p>
        )}
      </div>
      <div className="text-right">
        <p className={`text-sm font-semibold ${
          (asset.balance_current ?? 0) >= 0 ? 'text-slate-800' : 'text-red-600'
        }`}>
          {formatCurrency(asset.balance_current)}
        </p>
        {asset.balance_as_of && (
          <p className="text-xs text-slate-400">
            as of {new Date(asset.balance_as_of).toLocaleDateString()}
          </p>
        )}
      </div>
    </div>
  );
}

