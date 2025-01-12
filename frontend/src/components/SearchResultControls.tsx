import { SortBy } from "../types";
import SortBySelect from "./SortBySelect";

interface SearchResultControlsProps {
    numberOfResults: number;
    sortBy: SortBy;
    setSortBy: React.Dispatch<React.SetStateAction<SortBy>>;
}

export function SearchResultControls({
    numberOfResults,
    sortBy,
    setSortBy,
}: SearchResultControlsProps) {
    return (
        <div className="flex items-center gap-4 pb-2 pt-4">
            <SortBySelect sortBy={sortBy} setSortBy={setSortBy} />
            <p className="text-lg">
                <span className="font-bold">{numberOfResults}</span> results{" "}
                <span className="text-gray-200 px-4">|</span>
                Page 1 / 1
            </p>
        </div>
    );
}
