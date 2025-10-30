'use client';

import { useState } from 'react';

interface ToggleButtonProps {
  onToggle?: (isOn: boolean) => void;
}

const ToggleButton = ({ onToggle }: ToggleButtonProps) => {
  const [isFiltered, setIsFiltered] = useState(false);

  const handleToggle = () => {
    setIsFiltered(!isFiltered);
    onToggle?.(!isFiltered);
  };

  return (
    <div>
      <button onClick={handleToggle} className={`px-6 py-2 font-bold text-white rounded-md transition-colors duration-300 ease-in-out ${
        isFiltered ? 'bg-green-500' : 'bg-red-500'
      }`}>
        {isFiltered ? 'Filtered' : 'Unfiltered'}
      </button>
    </div>
  );
};

export default ToggleButton;
