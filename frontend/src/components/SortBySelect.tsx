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
                <SelectTrigger className="w-full">
                    <SelectValue />
                </SelectTrigger>
                <SelectContent>
                    <SelectGroup>
                        <SelectItem value="newest">Newest</SelectItem>
                        <SelectItem value="oldest">Oldest</SelectItem>
                        <SelectItem value="price_inc">
                            Price: Low to High
                        </SelectItem>
                        <SelectItem value="price_dec">
                            Price: High to Low
                        </SelectItem>
                    </SelectGroup>
                </SelectContent>
            </Select>
        </>
    );
}

export default SortBySelect;
