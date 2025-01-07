import { Location } from "../types";
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
    maxPrice: number;
    setMaxPrice: React.Dispatch<React.SetStateAction<number>>;
    minPrice: number;
    setMinPrice: React.Dispatch<React.SetStateAction<number>>;
    locations: Location[];
    locationFilters: Location[];
    setLocationFilters: React.Dispatch<React.SetStateAction<Location[]>>;
    keywords: string[];
    setKeywords: React.Dispatch<React.SetStateAction<string[]>>;
    updateFilters: () => void;
};

function FilterForm({
    sortBy,
    setSortBy,
    maxPrice,
    setMaxPrice,
    minPrice,
    setMinPrice,
    locations,
    locationFilters,
    setLocationFilters,
    keywords,
    setKeywords,
    updateFilters,
}: FilterFormProps) {
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
                            <SearchableMultiselect
                                locationFilters={locationFilters}
                                setLocationFilters={setLocationFilters}
                                locations={locations}
                            />
                        </FormInput>

                        <FormInput>
                            <Label htmlFor="minPrice maxPrice">Price</Label>
                            <MinMaxInput
                                unit="€"
                                minPrice={minPrice}
                                setMinPrice={setMinPrice}
                                maxPrice={maxPrice}
                                setMaxPrice={setMaxPrice}
                            />
                        </FormInput>

                        <FormInput>
                            <Label htmlFor="Custom keywords">
                                Custom keywords
                            </Label>
                            <KeywordAdder
                                keywords={keywords}
                                setKeywords={setKeywords}
                            />
                        </FormInput>

                        <FormInput>
                            <Button onClick={updateFilters}>
                                Update filters
                            </Button>
                        </FormInput>
                    </div>
                </CardContent>
            </Card>
        </>
    );
}

export default FilterForm;
