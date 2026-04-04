# Kolding Kommune

Support for schedules provided by [Kolding Kommune](https://kolding.dk/), serving Kolding municipality, Denmark.

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
    sources:
    - name: kolding_dk
      args:
        id: See description
```

### Configuration Variables

**id**  
_(String) (required)_

## Example

```yaml
waste_collection_schedule:
    sources:
    - name: kolding_dk
      args:
        id: "00007b8d-0002-0001-4164-647265737320"
```

## How to get the id

    To get your UUID (Geolocation) ID:
    1. Go to the [Kolding Kommune Min Side](https://kolding.dk/) page and navigate to waste collection services. 
    2. or go directly to : https://kolding.infovision.dk/public/selectaddress
    3. Search for your address.
    4. You will find your ID in URL i.e. : https://kolding.infovision.dk/public/address/00007b8d-0002-0001-4164-647265737320
    5. The ID should be a UUID format like: `00007b8d-0002-0001-4164-647265737320`
