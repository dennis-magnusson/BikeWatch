import { Location } from "../types";
import FormInput from "./FormInput";
import MinMaxInput from "./MinMaxInput";
import SearchableMultiselect from "./SearchableMultiselect";
import { SizeSelector } from "./SizeSelector";
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
    size: number;
    setSize: React.Dispatch<React.SetStateAction<number>>;
    showAllSizes: boolean;
    setShowAllSizes: React.Dispatch<React.SetStateAction<boolean>>;
    updateFilters: () => void;
    sizeFlexibility: boolean;
    setSizeFlexibility: React.Dispatch<React.SetStateAction<boolean>>;
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
    size,
    setSize,
    showAllSizes,
    setShowAllSizes,
    updateFilters,
    sizeFlexibility,
    setSizeFlexibility,
}: FilterFormProps) {
    return (
        <>
            <Card>
                <CardHeader>
                    <h2 className="font-bold text-3xl">Filter</h2>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-col w-full">
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

                        {/* <FormInput>
                            <Label htmlFor="Custom keywords">
                                Custom keywords
                            </Label>
                            <KeywordAdder
                                keywords={keywords}
                                setKeywords={setKeywords}
                            />
                        </FormInput> */}

                        <FormInput>
                            <Label htmlFor="size">Size</Label>
                            <SizeSelector
                                size={size}
                                setSize={setSize}
                                showAllSizes={showAllSizes}
                                setShowAllSizes={setShowAllSizes}
                                sizeFlexibility={sizeFlexibility}
                                setSizeFlexibility={setSizeFlexibility}
                            />
                        </FormInput>

                        <div className="pt-4">
                            <FormInput>
                                <Button onClick={updateFilters}>
                                    Update filters
                                </Button>
                            </FormInput>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </>
    );
}

export default FilterForm;
