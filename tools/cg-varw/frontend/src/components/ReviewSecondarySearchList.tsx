import { useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";

export function ReviewSecondarySearchList<T>({
  title,
  subtitle,
  items,
  selectedId,
  onSelect,
  getId,
  getSearchText,
  getItemClassName,
  renderItem,
  searchPlaceholder,
  resetKey,
  actions,
  loading = false,
  error = "",
  emptyText = "没有二级对象",
}: {
  title: string;
  subtitle?: string;
  items: T[];
  selectedId: string;
  onSelect: (item: T) => void;
  getId: (item: T) => string;
  getSearchText: (item: T) => string;
  getItemClassName?: (item: T) => string;
  renderItem: (item: T) => ReactNode;
  searchPlaceholder: string;
  resetKey: string;
  actions?: ReactNode;
  loading?: boolean;
  error?: string;
  emptyText?: string;
}) {
  const [query, setQuery] = useState("");

  useEffect(() => {
    setQuery("");
  }, [resetKey]);

  const normalizedQuery = query.trim().toLowerCase();
  const filteredItems = useMemo(
    () => normalizedQuery ? items.filter((item) => getSearchText(item).toLowerCase().includes(normalizedQuery)) : items,
    [getSearchText, items, normalizedQuery],
  );

  return (
    <section className="editor-section unit-queue-panel">
      <div className="section-title-row">
        <h3>{title}</h3>
        {subtitle && <span>{subtitle}</span>}
      </div>
      {actions}
      <div className="search-box">
        <span>⌕</span>
        <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder={searchPlaceholder} />
      </div>
      <div className="unit-queue">
        {loading && <div className="list-state">正在加载...</div>}
        {error && <div className="list-state list-state-error">{error}</div>}
        {!loading && !error && filteredItems.length === 0 && <div className="list-state">{emptyText}</div>}
        {!loading && !error && filteredItems.map((item) => {
          const id = getId(item);
          return (
            <button key={id} className={`unit-row ${selectedId === id ? "selected" : ""} ${getItemClassName?.(item) ?? ""}`} onClick={() => onSelect(item)}>
              {renderItem(item)}
            </button>
          );
        })}
      </div>
    </section>
  );
}
