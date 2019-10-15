# Contact! forms and s3 policies

## How to add a new form to contact app:

1. Create model (`models.py`) to store form submissions.
    * `db_table` name should start with 'contact_' with the class name represented after the underscore. Example: `class EmailTemplate` would be `db_table = 'contact_email_template'`
    * Primary Key UUID field like all other API models
    * Frontend form field names will be the 'keys' of the dictionary/object submitted to the contact app. The model fields must mimic these 'keys' but with the proper formatting. Model fields are expected to be formatted as **all lowercase** and **spaces replaced with underscores** versions of the frontend form fields/keys. Example: form field `First Name` must be model field `first_name`.
2. Create serializer (`serializers.py`) pointing to the new model. Will most likely use `__all__` fields.
3. Add model to `../dashboard.py` "Contact!" section by appending to the models list.
4. Register the model to to the admin console (`admin.py`). Aside from routine property configuration (list_display, ordering, etc.), **set all fields read only** so that form submissions cannot be overwritten or edited from their original values. Use other contact admin registrations' `get_readonly_fields` function as an example to accomplish this.
    * Contact tables serve as a record/log of submissions and their integrity is compromised when they are editable.
5. Migrate new model or changes to the database. Then spin up the API locally.
6. Open admin console and add a new record to the 'Email Templates' table in the 'Contact!' section. Save when done.
    *  **Email Template Type** is just a casual representation of the model class name. Used for reference only, not used programmatically.
    *  **Form ID** is the `form_id` from the frontend. This value must match the value for key `form_id` as submitted by the frontend to the submit API endpoint.
    *  **Sendpoint** is super important. This declares the address where the associated email for the form is sent. Use the dropdown to choose the literal key name (as in the submission object) of the destination address to send the response email.
        *  Choosing `default` from the dropdown will send the email to Support System and create a ticket.
        *  Choosing another value will send the email to that value as submitted in the form (most commonly this is a response email for things like event registration confirmations or forwarding outside entity messages automatically).
        *  Add a new forms' key to the sendpoint dropdown by editing the EmailTemplate model choices for said field.
    *  **Serializer Classname** is the class name from of the serializer created in #2. **MUST BE EXACT**. In order to keep the API endpoint apathetic, this field provides reference for importing as necessary.
    *  **Email Template Subject** is the subject of the email that will be sent (either to the ticketing system or another sendpoint as declared).
    *  **Email Template Body** is the body of the email that will be sent (either to the ticketing system or another sendpoint as declared).
        *  Form field values can be used within this template by wrapping the database field name (lowercased/underscored) with double curly brackets and no between them. Example: form field `First Name` can be used in the template as `{{first_name}}`.
        *  Although not necessary to include based on purpose served, default email body text includes the universally-applied `url` and always present `form_id` fields to help standard meta information get into the ticketing system
7.  Create the form on the frontend. Note the following rules:
    * `form_id` key must be within the submission object.
    * The value for the `form_id` key must match an Email Template record which exists in the database.
    * `recaptcha` key must be within the submission object.
    * The value for the `recaptcha` key must be a valid 'recapthca response token' as awarded to the form from user recaptcha completion. The response token will be verified within the API endpoint and if verification fails, a 400 Bad Request error will be returned to the client frontend.
    * Note: API utilizes the value of submission object key `email` for the 'reply to' email address. Essentially, submission handling assumes the form field `email` is that of the submitter and uses it for 'reply to' when sending the email. If `email` is not present, an empty string is used for the 'reply to'.

## Submit Form API Endpoint

All forms share the same API endpoint (SubmitFormViewSet) for handling form submissions (`viewsets.py`). This endpoint is apathetic to the form source. It will result in saving a record to the proper database table and sending the associated email as long as the following rules are adhered to:
* Model field names match frontend but with lowercasing and underscores as mentioned above in #1.
* `form_id` key is present in submission and an EmailTemplate is present with the matching form_id.
* `recaptcha` key is present in the submission and it's value successfully verifies with the recaptcha system.
* The proper `Serializer Classname` is correctly declared for the Email Template and the submission object has keys which successfully format to database fields.
* The proper `sendpoint` is declared for the Email Template. `default` will create a ticket in the ticketing system whereas any other sendpoint assumes that sendpoint is a key in the submission object and uses the value of that key as the address to send the email to.

## s3 Policy API Endpoints

These endpoints (zip, image, general) are used to create temporary signatures for client side uploads to s3. When hit, the endpoint generates and returns a 'signed policy' object which has three values to be used in the header of the upload. A properly encoded 'policy', 'signature', and 'key' declare metadata (format suffix, data type, file size, expiration time, etc.) for the file being uploaded and, when attached to the client's upload, permit the user to directly upload files to a private s3 bucket. This allows their files to be stored in the cloud and privately accessible from TNRIS after the form is submitted.

## CORS API Whitelist & s3 Bucket CORS Config

* An additional, custom CORS security measure is applied directly within the API endpoint 'permission classes'. The request's `HTTP_HOST` Meta property is verified against a list of permitted domains managed within `viewsets.py`. Add or remove domains from this `whitelisted_domains` variable to alter permitted hosts to use the Contact API Endpoints.
* The s3 bucket used for signed-policy client side uploads has a CORS configuration applied which restricts uploads to applications running under the tnris.org wildcard SSL certificate. This means that local development form uploads will fail unless this s3 bucket CORS is temporarily disabled. Open the bucket properties within the AWS console to manage this CORS configuration.

## Recaptcha

Recaptcha must be used for all form submissions. Currently implemented is v2 Checkbox. The submission API endpoint will return a 400 error BAD REQUEST for all non-existent or invalid recaptcha response tokens in submission objects. Visit the Google Recaptcha website within the browser and sign in using the TNRIS account to manage recaptcha keys.