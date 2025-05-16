# Security Recommendations for JamiBilling

## Database Credentials

Currently, the application stores database credentials in `config.json`. For improved security, consider these alternatives:

1. **Environment Variables**: 
   - Store credentials as environment variables
   - Update app.py to use `os.environ.get()` to access them
   - Example:
     ```python
     server = os.environ.get('JAMI_DB_SERVER')
     database = os.environ.get('JAMI_DB_NAME')
     username = os.environ.get('JAMI_DB_USERNAME')
     password = os.environ.get('JAMI_DB_PASSWORD')
     ```

2. **Encrypted Configuration**:
   - Encrypt sensitive parts of config.json
   - Use a separate key that's not stored in the repository
   - Example tools: python-dotenv with encryption or Azure Key Vault integration

## RDN Credentials

User credentials for RDN are currently stored in the session. For additional security:

1. **Session Timeout**: 
   - Implement shorter session timeouts for security
   - Add `app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=30)` 

2. **HTTPS**:
   - Always use HTTPS in production
   - Add Flask-SSLify for enforcing HTTPS

## General Recommendations

1. **Input Validation**:
   - Add validation for all user inputs
   - Sanitize inputs to prevent SQL injection and XSS

2. **Access Controls**:
   - Implement proper authentication
   - Add role-based access control if multiple user types exist

3. **Rate Limiting**:
   - Add rate limiting for login attempts
   - Consider using Flask-Limiter

4. **Audit Logging**:
   - Enhance logging with audit trails
   - Log all sensitive operations without including actual credentials

5. **Regular Updates**:
   - Keep all dependencies updated
   - Regularly check for security vulnerabilities