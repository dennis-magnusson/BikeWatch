import FormInput from "./FormInput";
import KeywordAdder from "./KeywordAdder";
import MinMaxInput from "./MinMaxInput";
import SearchableMultiselect from "./SearchableMultiselect";
import SortBySelect from "./SortBySelect";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader } from "./ui/card";
import { Label } from "./ui/label";

type FilterFormProps = {
    sortBy: string;
    setSortBy: React.Dispatch<React.SetStateAction<string>>;
};

function FilterForm({ sortBy, setSortBy }: FilterFormProps) {
    return (
        <>
            <Card>
                <CardHeader>
                    <h2 className="font-bold text-3xl">Filter</h2>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-col min-w-[280px]">
                        <FormInput>
                            <Label htmlFor="sort">Sort by</Label>
                            <SortBySelect
                                sortBy={sortBy}
                                setSortBy={setSortBy}
                            />
                        </FormInput>

                        <FormInput>
                            <Label htmlFor="city">Location</Label>
                            <SearchableMultiselect />
                        </FormInput>

                        <FormInput>
                            <Label htmlFor="minPrice maxPrice">Price</Label>
                            <MinMaxInput unit="€" />
                        </FormInput>

                        <FormInput>
                            <Label htmlFor="Custom keywords">
                                Custom keywords
                            </Label>
                            <KeywordAdder />
                        </FormInput>

                        <FormInput>
                            <Button>Update filters</Button>
                        </FormInput>
                    </div>
                </CardContent>
            </Card>
        </>
    );
}

export default FilterForm;
