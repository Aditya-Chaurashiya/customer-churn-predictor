import React from 'react';
import clsx from 'clsx';

interface RiskBadgeProps {
  level: 'Low' | 'Medium' | 'High' | 'Critical';
}

const riskStyles = {
  Low: 'bg-green-100 text-green-800',
  Medium: 'bg-yellow-100 text-yellow-800',
  High: 'bg-orange-100 text-orange-800',
  Critical: 'bg-red-100 text-red-800',
};

export default function RiskBadge({ level }: RiskBadgeProps) {
  return (
    <span className={clsx('px-2.5 py-0.5 rounded-full text-xs font-medium', riskStyles[level] || 'bg-gray-100 text-gray-800')}>
      {level} Risk
    </span>
  );
}
