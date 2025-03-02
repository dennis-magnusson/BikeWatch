import { SortBy } from "../types";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "./ui/select";

type SortBySelectProps = {
    sortBy: SortBy;
    setSortBy: React.Dispatch<React.SetStateAction<SortBy>>;
};

function SortBySelect({ sortBy, setSortBy }: SortBySelectProps) {
    const handleValueChange = (value: string) => {
        setSortBy(value as SortBy);
    };
    return (
        <>
            <Select value={sortBy} onValueChange={handleValueChange}>
                <SelectTrigger className="w-48">
                    <SelectValue />
                </SelectTrigger>
                <SelectContent>
                    <SelectGroup>
                        <SelectItem value="newest">Newest first</SelectItem>
                        <SelectItem value="oldest">Oldest first</SelectItem>
                        <SelectItem value="price_inc">
                            Price ascending
                        </SelectItem>
                        <SelectItem value="price_dec">
                            Price descending
                        </SelectItem>
                    </SelectGroup>
                </SelectContent>
            </Select>
        </>
    );
}

export default SortBySelect;
