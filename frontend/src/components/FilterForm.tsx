import { CATEGORIES } from "../constants";
import { Location } from "../types";
import CheckboxGroup from "./CheckboxGroup";
import FormInput from "./FormInput";
import KeywordAdder from "./KeywordAdder";
import MinMaxInput from "./MinMaxInput";
import SearchableMultiselect from "./SearchableMultiselect";
import { SizeSelector } from "./SizeSelector";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader } from "./ui/card";
import { Label } from "./ui/label";

type FilterFormProps = {
    maxPrice: number;
    setMaxPrice: React.Dispatch<React.SetStateAction<number>>;
    minPrice: number;
    setMinPrice: React.Dispatch<React.SetStateAction<number>>;
    hasError: boolean;
    setHasError: React.Dispatch<React.SetStateAction<boolean>>;
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
    keywords: string[];
    setKeywords: React.Dispatch<React.SetStateAction<string[]>>;
    selectedCategories: string[];
    setSelectedCategories: React.Dispatch<React.SetStateAction<string[]>>;
    resetSearchFilters: () => void;
    resetButtonDisabled: boolean;
};

function FilterForm({
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
    keywords,
    setKeywords,
    selectedCategories,
    setSelectedCategories,
    resetSearchFilters,
    resetButtonDisabled,
    hasError,
    setHasError,
}: FilterFormProps) {
    const validatePrices = () => {
        if (minPrice > maxPrice) {
            setHasError(true);
            return false;
        }
        setHasError(false);
        return true;
    };

    const handleUpdateFilters = () => {
        if (validatePrices()) {
            updateFilters();
        }
    };

    const handleResetFilters = () => {
        setHasError(false);
        resetSearchFilters();
    };

    const categoryOptions = CATEGORIES.map((c) => ({
        id: c,
        value: c,
        label: (c.charAt(0).toUpperCase() + c.slice(1)).replace("_", " "),
    }));

    return (
        <div className="w-full">
            <Card>
                <CardHeader>
                    <h2 className="font-bold text-3xl">Search for bicycles</h2>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-row space-x-16">
                        <div>
                            <FormInput>
                                <CheckboxGroup
                                    label="Type"
                                    options={categoryOptions}
                                    selectedOptions={selectedCategories}
                                    setSelectedOptions={setSelectedCategories}
                                />
                            </FormInput>
                        </div>
                        <div>
                            <FormInput>
                                <Label
                                    htmlFor="minPrice maxPrice"
                                    className="text-base"
                                >
                                    Price
                                </Label>
                                <MinMaxInput
                                    unit="€"
                                    minPrice={minPrice}
                                    setMinPrice={setMinPrice}
                                    maxPrice={maxPrice}
                                    setMaxPrice={setMaxPrice}
                                    validatePrices={validatePrices}
                                    hasError={hasError}
                                />
                            </FormInput>
                            <FormInput>
                                <Label htmlFor="size" className="text-base">
                                    Size
                                </Label>
                                <SizeSelector
                                    size={size}
                                    setSize={setSize}
                                    showAllSizes={showAllSizes}
                                    setShowAllSizes={setShowAllSizes}
                                    sizeFlexibility={sizeFlexibility}
                                    setSizeFlexibility={setSizeFlexibility}
                                />
                            </FormInput>
                        </div>
                        <div>
                            <FormInput>
                                <Label htmlFor="city" className="text-base">
                                    Location
                                </Label>
                                <SearchableMultiselect
                                    locationFilters={locationFilters}
                                    setLocationFilters={setLocationFilters}
                                    locations={locations}
                                />
                            </FormInput>
                            <FormInput>
                                <Label
                                    htmlFor="Custom keywords"
                                    className="text-base"
                                >
                                    Custom keywords
                                </Label>
                                <KeywordAdder
                                    keywords={keywords}
                                    setKeywords={setKeywords}
                                />
                            </FormInput>
                        </div>
                    </div>

                    <div className="w-52 mt-4">
                        <Button onClick={handleUpdateFilters}>
                            Update filters
                        </Button>{" "}
                        <Button
                            variant={"outline"}
                            onClick={handleResetFilters}
                            disabled={resetButtonDisabled}
                        >
                            Reset
                        </Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}

export default FilterForm;
