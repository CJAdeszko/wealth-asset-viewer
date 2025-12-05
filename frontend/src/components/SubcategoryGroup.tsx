import { useState } from 'react';
import type { Asset } from '../types/asset';
import { formatCurrency } from '../utils/format';
import { AssetItem } from './AssetItem';

interface SubcategoryGroupProps {
  name: string;
  total: number;
  assets: Asset[];
}

export function SubcategoryGroup({ name, total, assets }: SubcategoryGroupProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  
  return (
    <div className="border-b border-slate-200 last:border-b-0">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between py-3 px-4 bg-slate-50 hover:bg-slate-100 transition-colors text-left"
      >
        <div className="flex items-center gap-3">
          <svg
            className={`w-4 h-4 text-slate-500 transition-transform duration-200 ${
              isExpanded ? 'rotate-90' : ''
            }`}
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
          <span className="text-sm font-medium text-slate-600">{name || 'Uncategorized'}</span>
          <span className="text-xs text-slate-400 bg-slate-200 px-2 py-0.5 rounded-full">
            {assets.length}
          </span>
        </div>
        <span className="text-sm font-semibold text-slate-700">
          {formatCurrency(total)}
        </span>
      </button>
      
      <div
        className={`overflow-hidden transition-all duration-200 ${
          isExpanded ? 'max-h-[2000px] opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="ml-6 border-l-2 border-slate-200">
          {assets.map((asset) => (
            <AssetItem key={asset.wid} asset={asset} />
          ))}
        </div>
      </div>
    </div>
  );
}

