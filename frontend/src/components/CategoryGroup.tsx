import { useState } from 'react';
import type { Asset } from '../types/asset';
import { formatCurrency } from '../utils/format';
import { SubcategoryGroup } from './SubcategoryGroup';

interface SubcategoryData {
  total: number;
  assets: Asset[];
}

interface CategoryGroupProps {
  name: string;
  total: number;
  subcategories: Record<string, SubcategoryData>;
}

export function CategoryGroup({ name, total, subcategories }: CategoryGroupProps) {
  const [isExpanded, setIsExpanded] = useState(true);
  
  const subcategoryEntries = Object.entries(subcategories).sort(([a], [b]) => 
    (a || 'zzz').localeCompare(b || 'zzz')
  );
  
  const totalAssets = subcategoryEntries.reduce(
    (sum, [, data]) => sum + data.assets.length,
    0
  );
  
  return (
    <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden mb-4">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between py-4 px-5 bg-primary-900 hover:bg-primary-800 transition-colors text-left"
      >
        <div className="flex items-center gap-3">
          <svg
            className={`w-5 h-5 text-primary-200 transition-transform duration-200 ${
              isExpanded ? 'rotate-90' : ''
            }`}
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
          <span className="text-base font-semibold text-white">{name || 'Uncategorized'}</span>
          <span className="text-xs text-primary-300 bg-primary-800 px-2 py-0.5 rounded-full">
            {totalAssets} {totalAssets === 1 ? 'asset' : 'assets'}
          </span>
        </div>
        <span className="text-lg font-bold text-white">
          {formatCurrency(total)}
        </span>
      </button>
      
      <div
        className={`overflow-hidden transition-all duration-300 ${
          isExpanded ? 'max-h-[5000px] opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        {subcategoryEntries.map(([subcategoryName, data]) => (
          <SubcategoryGroup
            key={subcategoryName}
            name={subcategoryName}
            total={data.total}
            assets={data.assets}
          />
        ))}
      </div>
    </div>
  );
}

