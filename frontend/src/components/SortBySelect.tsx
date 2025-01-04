import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "./ui/select";

type SortBySelectProps = {
    sortBy: string;
    setSortBy: React.Dispatch<React.SetStateAction<string>>;
};

function SortBySelect({ sortBy, setSortBy }: SortBySelectProps) {
    return (
        <>
            <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger className="w-[180px]">
                    <SelectValue />
                </SelectTrigger>
                <SelectContent>
                    <SelectGroup>
                        <SelectItem value="price_low-high">
                            Price: Low to High
                        </SelectItem>
                        <SelectItem value="price_high-low">
                            Price: High to Low
                        </SelectItem>
                        <SelectItem value="newest">Newest</SelectItem>
                        <SelectItem value="oldest">Oldest</SelectItem>
                        <SelectItem value="most_popular">
                            Most Popular
                        </SelectItem>
                    </SelectGroup>
                </SelectContent>
            </Select>
        </>
    );
}

export default SortBySelect;
