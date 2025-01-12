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
