'use client';

import { useEffect, useRef, useState } from 'react';

interface ToggleButtonProps {
  isFiltered: boolean;
  onToggle?: (isOn: boolean) => void;
}

const ToggleButton = ({ isFiltered, onToggle }: ToggleButtonProps) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  const handleToggle = () => {
    onToggle?.(!isFiltered);
  };

  const handleMenuToggle = () => {
    setIsMenuOpen((prev) => !prev);
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsMenuOpen(false);
      }
    };

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsMenuOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEscape);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, []);

  return (
    <div ref={menuRef} className="relative inline-block text-left">
      <button
        onClick={handleMenuToggle}
        type="button"
        className="rounded-md border border-border bg-card px-4 py-2 text-sm font-medium text-foreground shadow-sm transition-colors hover:bg-muted"
      >
        Settings
      </button>

      {isMenuOpen && (
        <div className="absolute right-0 bottom-full z-10 mb-2 w-64 origin-bottom-right rounded-lg border border-border bg-background shadow-lg">
          <div className="p-4 space-y-3">
            <div className="flex flex-col">
              <span className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                Moderation mode
              </span>
              <span className="text-base font-semibold text-foreground">
                {isFiltered ? 'Filtered' : 'Unfiltered'}
              </span>
            </div>

            <button
              onClick={handleToggle}
              type="button"
              className="w-full rounded-md bg-primary px-3 py-2 text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90"
            >
              Switch to {isFiltered ? 'Unfiltered' : 'Filtered'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ToggleButton;
