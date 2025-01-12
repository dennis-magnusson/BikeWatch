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
    bikeTypes: string[];
    setBikeTypes: React.Dispatch<React.SetStateAction<string[]>>;
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
    bikeTypes,
    setBikeTypes,
}: FilterFormProps) {
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
                                <CheckboxGroup
                                    label="Type"
                                    options={[
                                        {
                                            id: "road",
                                            value: "road",
                                            label: "Road",
                                        },
                                        {
                                            id: "gravel",
                                            value: "gravel",
                                            label: "Gravel",
                                        },
                                        {
                                            id: "triathlon",
                                            value: "triathlon",
                                            label: "Triathlon",
                                        },
                                        {
                                            id: "hybrid",
                                            value: "hybrid",
                                            label: "Hybrid",
                                        },
                                        {
                                            id: "mountain",
                                            value: "mountain",
                                            label: "Mountain",
                                        },
                                        {
                                            id: "fatbike",
                                            value: "fatbike",
                                            label: "Fatbike",
                                        },
                                        {
                                            id: "kids",
                                            value: "kids",
                                            label: "Kids",
                                        },
                                        {
                                            id: "electric",
                                            value: "electric",
                                            label: "Electric",
                                        },
                                        {
                                            id: "other",
                                            value: "other",
                                            label: "Other",
                                        },
                                    ]}
                                    selectedOptions={bikeTypes}
                                    setSelectedOptions={setBikeTypes}
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
                        <Button onClick={updateFilters} disabled={false}>
                            Update filters
                        </Button>{" "}
                        <Button variant={"outline"}>Reset</Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}

export default FilterForm;
