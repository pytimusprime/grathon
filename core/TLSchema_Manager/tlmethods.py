from typing import Any, List, Optional, Union
import asyncio
from grathon.core.TLSchema_Manager.tltypes import *

class GeneratedMethods:
    def __init__(self, client):
        self._client = client

    async def get_authorization_state(self) -> AuthorizationState:
        """
        description Returns the current authorization state. This is an offline method. For informational purposes only. Use updateAuthorizationState instead to maintain the current authorization state. Can be called before initialization
        """
        return await self._client.call_method('getAuthorizationState', {'@type': 'getAuthorizationState'})

    async def set_tdlib_parameters(self, use_test_dc: bool = None, database_directory: str = None, files_directory: str = None, database_encryption_key: bytes = None, use_file_database: bool = None, use_chat_info_database: bool = None, use_message_database: bool = None, use_secret_chats: bool = None, api_id: int = None, api_hash: str = None, system_language_code: str = None, device_model: str = None, system_version: str = None, application_version: str = None) -> Ok:
        """
        description Sets the parameters for TDLib initialization. Works only when the current authorization state is authorizationStateWaitTdlibParameters
        use_test_dc Pass true to use Telegram test environment instead of the production environment
        database_directory The path to the directory for the persistent database; if empty, the current working directory will be used
        files_directory The path to the directory for storing files; if empty, database_directory will be used
        database_encryption_key Encryption key for the database. If the encryption key is invalid, then an error with code 401 will be returned
        use_file_database Pass true to keep information about downloaded and uploaded files between application restarts
        use_chat_info_database Pass true to keep cache of users, basic groups, supergroups, channels and secret chats between restarts. Implies use_file_database
        use_message_database Pass true to keep cache of chats and messages between restarts. Implies use_chat_info_database
        use_secret_chats Pass true to enable support for secret chats
        api_id Application identifier for Telegram API access, which can be obtained at https://my.telegram.org
        api_hash Application identifier hash for Telegram API access, which can be obtained at https://my.telegram.org
        system_language_code IETF language tag of the user's operating system language; must be non-empty
        device_model Model of the device the application is being run on; must be non-empty
        system_version Version of the operating system the application is being run on. If empty, the version is automatically detected by TDLib
        application_version Application version; must be non-empty
        """
        return await self._client.call_method('setTdlibParameters', {'@type': 'setTdlibParameters', 'use_test_dc': use_test_dc, 'database_directory': database_directory, 'files_directory': files_directory, 'database_encryption_key': database_encryption_key, 'use_file_database': use_file_database, 'use_chat_info_database': use_chat_info_database, 'use_message_database': use_message_database, 'use_secret_chats': use_secret_chats, 'api_id': api_id, 'api_hash': api_hash, 'system_language_code': system_language_code, 'device_model': device_model, 'system_version': system_version, 'application_version': application_version})

    async def set_authentication_phone_number(self, phone_number: str = None, settings: phoneNumberAuthenticationSettings = None) -> Ok:
        """
        description Sets the phone number of the user and sends an authentication code to the user. Works only when the current authorization state is authorizationStateWaitPhoneNumber,
        phone_number The phone number of the user, in international format
        settings Settings for the authentication of the user's phone number; pass null to use default settings
        """
        return await self._client.call_method('setAuthenticationPhoneNumber', {'@type': 'setAuthenticationPhoneNumber', 'phone_number': phone_number, 'settings': settings})

    async def check_authentication_premium_purchase(self, premium_day_count: int = None, currency: str = None, amount: int = None) -> Ok:
        """
        description Checks whether an in-store purchase of Telegram Premium is possible before authorization. Works only when the current authorization state is authorizationStateWaitPremiumPurchase
        premium_day_count The number of days for which the Telegram Premium subscription will be granted
        currency ISO 4217 currency code of the payment currency
        amount Paid amount, in the smallest units of the currency
        """
        return await self._client.call_method('checkAuthenticationPremiumPurchase', {'@type': 'checkAuthenticationPremiumPurchase', 'premium_day_count': premium_day_count, 'currency': currency, 'amount': amount})

    async def set_authentication_premium_purchase_transaction(self, transaction: StoreTransaction = None, is_restore: bool = None, premium_day_count: int = None, currency: str = None, amount: int = None) -> Ok:
        """
        description Informs server about an in-store purchase of Telegram Premium before authorization. Works only when the current authorization state is authorizationStateWaitPremiumPurchase
        transaction Information about the transaction
        is_restore Pass true if this is a restore of a Telegram Premium purchase; only for App Store
        premium_day_count The number of days for which the Telegram Premium subscription will be granted
        currency ISO 4217 currency code of the payment currency
        amount Paid amount, in the smallest units of the currency
        """
        return await self._client.call_method('setAuthenticationPremiumPurchaseTransaction', {'@type': 'setAuthenticationPremiumPurchaseTransaction', 'transaction': transaction, 'is_restore': is_restore, 'premium_day_count': premium_day_count, 'currency': currency, 'amount': amount})

    async def set_authentication_email_address(self, email_address: str = None) -> Ok:
        """
        description Sets the email address of the user and sends an authentication code to the email address. Works only when the current authorization state is authorizationStateWaitEmailAddress @email_address The email address of the user
        """
        return await self._client.call_method('setAuthenticationEmailAddress', {'@type': 'setAuthenticationEmailAddress', 'email_address': email_address})

    async def resend_authentication_code(self, reason: ResendCodeReason = None) -> Ok:
        """
        description Resends an authentication code to the user. Works only when the current authorization state is authorizationStateWaitCode, the next_code_type of the result is not null
        reason Reason of code resending; pass null if unknown
        """
        return await self._client.call_method('resendAuthenticationCode', {'@type': 'resendAuthenticationCode', 'reason': reason})

    async def check_authentication_email_code(self, code: EmailAddressAuthentication = None) -> Ok:
        """
        description Checks the authentication of an email address. Works only when the current authorization state is authorizationStateWaitEmailCode @code Email address authentication to check
        """
        return await self._client.call_method('checkAuthenticationEmailCode', {'@type': 'checkAuthenticationEmailCode', 'code': code})

    async def check_authentication_code(self, code: str = None) -> Ok:
        """
        description Checks the authentication code. Works only when the current authorization state is authorizationStateWaitCode @code Authentication code to check
        """
        return await self._client.call_method('checkAuthenticationCode', {'@type': 'checkAuthenticationCode', 'code': code})

    async def request_qr_code_authentication(self, other_user_ids: List[int] = None) -> Ok:
        """
        description Requests QR code authentication by scanning a QR code on another logged in device. Works only when the current authorization state is authorizationStateWaitPhoneNumber,
        other_user_ids List of user identifiers of other users currently using the application
        """
        return await self._client.call_method('requestQrCodeAuthentication', {'@type': 'requestQrCodeAuthentication', 'other_user_ids': other_user_ids})

    async def get_authentication_passkey_parameters(self) -> Text:
        """
        description Returns parameters for authentication using a passkey as JSON-serialized string
        """
        return await self._client.call_method('getAuthenticationPasskeyParameters', {'@type': 'getAuthenticationPasskeyParameters'})

    async def check_authentication_passkey(self, credential_id: str = None, client_data: str = None, authenticator_data: bytes = None, signature: bytes = None, user_handle: bytes = None) -> Ok:
        """
        description Checks a passkey to log in to the corresponding account. Call getAuthenticationPasskeyParameters to get parameters for the passkey. Works only when the current authorization state is
        credential_id Base64url-encoded identifier of the credential
        client_data JSON-encoded client data
        authenticator_data Authenticator data of the application that created the credential
        signature Cryptographic signature of the credential
        user_handle User handle of the passkey
        """
        return await self._client.call_method('checkAuthenticationPasskey', {'@type': 'checkAuthenticationPasskey', 'credential_id': credential_id, 'client_data': client_data, 'authenticator_data': authenticator_data, 'signature': signature, 'user_handle': user_handle})

    async def check_authentication_web_token(self, token: str = None, dc_id: int = None) -> Ok:
        """
        description Checks a web token to log in to the corresponding account; for official Telegram apps only. Works only when the current authorization state is
        token The token to check
        dc_id Identifier of the datacenter of the user
        """
        return await self._client.call_method('checkAuthenticationWebToken', {'@type': 'checkAuthenticationWebToken', 'token': token, 'dc_id': dc_id})

    async def register_user(self, first_name: str = None, last_name: str = None, disable_notification: bool = None) -> Ok:
        """
        description Finishes user registration. Works only when the current authorization state is authorizationStateWaitRegistration
        first_name The first name of the user; 1-64 characters
        last_name The last name of the user; 0-64 characters
        disable_notification Pass true to disable notification about the current user joining Telegram for other users that added them to contact list
        """
        return await self._client.call_method('registerUser', {'@type': 'registerUser', 'first_name': first_name, 'last_name': last_name, 'disable_notification': disable_notification})

    async def reset_authentication_email_address(self) -> Ok:
        """
        description Resets the login email address. May return an error with a message "TASK_ALREADY_EXISTS" if reset is still pending.
        """
        return await self._client.call_method('resetAuthenticationEmailAddress', {'@type': 'resetAuthenticationEmailAddress'})

    async def check_authentication_password(self, password: str = None) -> Ok:
        """
        description Checks the 2-step verification password for correctness. Works only when the current authorization state is authorizationStateWaitPassword @password The 2-step verification password to check
        """
        return await self._client.call_method('checkAuthenticationPassword', {'@type': 'checkAuthenticationPassword', 'password': password})

    async def request_authentication_password_recovery(self) -> Ok:
        """
        description Requests to send a 2-step verification password recovery code to an email address that was previously set up. Works only when the current authorization state is authorizationStateWaitPassword
        """
        return await self._client.call_method('requestAuthenticationPasswordRecovery', {'@type': 'requestAuthenticationPasswordRecovery'})

    async def check_authentication_password_recovery_code(self, recovery_code: str = None) -> Ok:
        """
        description Checks whether a 2-step verification password recovery code sent to an email address is valid. Works only when the current authorization state is authorizationStateWaitPassword @recovery_code Recovery code to check
        """
        return await self._client.call_method('checkAuthenticationPasswordRecoveryCode', {'@type': 'checkAuthenticationPasswordRecoveryCode', 'recovery_code': recovery_code})

    async def recover_authentication_password(self, recovery_code: str = None, new_password: str = None, new_hint: str = None) -> Ok:
        """
        description Recovers the 2-step verification password with a password recovery code sent to an email address that was previously set up. Works only when the current authorization state is authorizationStateWaitPassword
        recovery_code Recovery code to check
        new_password New 2-step verification password of the user; may be empty to remove the password
        new_hint New password hint; may be empty
        """
        return await self._client.call_method('recoverAuthenticationPassword', {'@type': 'recoverAuthenticationPassword', 'recovery_code': recovery_code, 'new_password': new_password, 'new_hint': new_hint})

    async def send_authentication_firebase_sms(self, token: str = None) -> Ok:
        """
        description Sends Firebase Authentication SMS to the phone number of the user. Works only when the current authorization state is authorizationStateWaitCode and the server returned code of the type authenticationCodeTypeFirebaseAndroid or authenticationCodeTypeFirebaseIos
        token Play Integrity API or SafetyNet Attestation API token for the Android application, or secret from push notification for the iOS application
        """
        return await self._client.call_method('sendAuthenticationFirebaseSms', {'@type': 'sendAuthenticationFirebaseSms', 'token': token})

    async def report_authentication_code_missing(self, mobile_network_code: str = None) -> Ok:
        """
        description Reports that authentication code wasn't delivered via SMS; for official mobile applications only. Works only when the current authorization state is authorizationStateWaitCode @mobile_network_code Current mobile network code
        """
        return await self._client.call_method('reportAuthenticationCodeMissing', {'@type': 'reportAuthenticationCodeMissing', 'mobile_network_code': mobile_network_code})

    async def check_authentication_bot_token(self, token: str = None) -> Ok:
        """
        description Checks the authentication token of a bot; to log in as a bot. Works only when the current authorization state is authorizationStateWaitPhoneNumber. Can be used instead of setAuthenticationPhoneNumber and checkAuthenticationCode to log in @token The bot token
        """
        return await self._client.call_method('checkAuthenticationBotToken', {'@type': 'checkAuthenticationBotToken', 'token': token})

    async def log_out(self) -> Ok:
        """
        description Closes the TDLib instance after a proper logout. Requires an available network connection. All local data will be destroyed. After the logout completes, updateAuthorizationState with authorizationStateClosed will be sent
        """
        return await self._client.call_method('logOut', {'@type': 'logOut'})

    async def close(self) -> Ok:
        """
        description Closes the TDLib instance. All databases will be flushed to disk and properly closed. After the close completes, updateAuthorizationState with authorizationStateClosed will be sent. Can be called before initialization
        """
        return await self._client.call_method('close', {'@type': 'close'})

    async def destroy(self) -> Ok:
        """
        description Closes the TDLib instance, destroying all local data without a proper logout. The current user session will remain in the list of all active sessions. All local data will be destroyed.
        """
        return await self._client.call_method('destroy', {'@type': 'destroy'})

    async def confirm_qr_code_authentication(self, link: str = None) -> Session:
        """
        description Confirms QR code authentication on another device. Returns created session on success @link A link from a QR code. The link must be scanned by the in-app camera
        """
        return await self._client.call_method('confirmQrCodeAuthentication', {'@type': 'confirmQrCodeAuthentication', 'link': link})

    async def get_current_state(self) -> Updates:
        """
        description Returns all updates needed to restore current TDLib state, i.e. all actual updateAuthorizationState/updateUser/updateNewChat and others. This is especially useful if TDLib is run in a separate process. Can be called before initialization
        """
        return await self._client.call_method('getCurrentState', {'@type': 'getCurrentState'})

    async def set_database_encryption_key(self, new_encryption_key: bytes = None) -> Ok:
        """
        description Changes the database encryption key. Usually the encryption key is never changed and is stored in some OS keychain @new_encryption_key New encryption key
        """
        return await self._client.call_method('setDatabaseEncryptionKey', {'@type': 'setDatabaseEncryptionKey', 'new_encryption_key': new_encryption_key})

    async def get_password_state(self) -> PasswordState:
        """
        description Returns the current state of 2-step verification
        """
        return await self._client.call_method('getPasswordState', {'@type': 'getPasswordState'})

    async def set_password(self, old_password: str = None, new_password: str = None, new_hint: str = None, set_recovery_email_address: bool = None, new_recovery_email_address: str = None) -> PasswordState:
        """
        description Changes the 2-step verification password for the current user. If a new recovery email address is specified, then the change will not be applied until the new recovery email address is confirmed
        old_password Previous 2-step verification password of the user
        new_password New 2-step verification password of the user; may be empty to remove the password
        new_hint New password hint; may be empty
        set_recovery_email_address Pass true to change also the recovery email address
        new_recovery_email_address New recovery email address; may be empty
        """
        return await self._client.call_method('setPassword', {'@type': 'setPassword', 'old_password': old_password, 'new_password': new_password, 'new_hint': new_hint, 'set_recovery_email_address': set_recovery_email_address, 'new_recovery_email_address': new_recovery_email_address})

    async def is_login_email_address_required(self) -> Ok:
        """
        description Checks whether the current user is required to set login email address
        """
        return await self._client.call_method('isLoginEmailAddressRequired', {'@type': 'isLoginEmailAddressRequired'})

    async def set_login_email_address(self, new_login_email_address: str = None) -> EmailAddressAuthenticationCodeInfo:
        """
        description Changes the login email address of the user. The email address can be changed only if the current user already has login email and passwordState.login_email_address_pattern is non-empty,
        new_login_email_address New login email address
        """
        return await self._client.call_method('setLoginEmailAddress', {'@type': 'setLoginEmailAddress', 'new_login_email_address': new_login_email_address})

    async def resend_login_email_address_code(self) -> EmailAddressAuthenticationCodeInfo:
        """
        description Resends the login email address verification code
        """
        return await self._client.call_method('resendLoginEmailAddressCode', {'@type': 'resendLoginEmailAddressCode'})

    async def check_login_email_address_code(self, code: EmailAddressAuthentication = None) -> Ok:
        """
        description Checks the login email address authentication @code Email address authentication to check
        """
        return await self._client.call_method('checkLoginEmailAddressCode', {'@type': 'checkLoginEmailAddressCode', 'code': code})

    async def get_recovery_email_address(self, password: str = None) -> RecoveryEmailAddress:
        """
        description Returns a 2-step verification recovery email address that was previously set up. This method can be used to verify a password provided by the user @password The 2-step verification password for the current user
        """
        return await self._client.call_method('getRecoveryEmailAddress', {'@type': 'getRecoveryEmailAddress', 'password': password})

    async def set_recovery_email_address(self, password: str = None, new_recovery_email_address: str = None) -> PasswordState:
        """
        description Changes the 2-step verification recovery email address of the user. If a new recovery email address is specified, then the change will not be applied until the new recovery email address is confirmed.
        password The 2-step verification password of the current user
        new_recovery_email_address New recovery email address
        """
        return await self._client.call_method('setRecoveryEmailAddress', {'@type': 'setRecoveryEmailAddress', 'password': password, 'new_recovery_email_address': new_recovery_email_address})

    async def check_recovery_email_address_code(self, code: str = None) -> PasswordState:
        """
        description Checks the 2-step verification recovery email address verification code @code Verification code to check
        """
        return await self._client.call_method('checkRecoveryEmailAddressCode', {'@type': 'checkRecoveryEmailAddressCode', 'code': code})

    async def resend_recovery_email_address_code(self) -> PasswordState:
        """
        description Resends the 2-step verification recovery email address verification code
        """
        return await self._client.call_method('resendRecoveryEmailAddressCode', {'@type': 'resendRecoveryEmailAddressCode'})

    async def cancel_recovery_email_address_verification(self) -> PasswordState:
        """
        description Cancels verification of the 2-step verification recovery email address
        """
        return await self._client.call_method('cancelRecoveryEmailAddressVerification', {'@type': 'cancelRecoveryEmailAddressVerification'})

    async def request_password_recovery(self) -> EmailAddressAuthenticationCodeInfo:
        """
        description Requests to send a 2-step verification password recovery code to an email address that was previously set up
        """
        return await self._client.call_method('requestPasswordRecovery', {'@type': 'requestPasswordRecovery'})

    async def check_password_recovery_code(self, recovery_code: str = None) -> Ok:
        """
        description Checks whether a 2-step verification password recovery code sent to an email address is valid @recovery_code Recovery code to check
        """
        return await self._client.call_method('checkPasswordRecoveryCode', {'@type': 'checkPasswordRecoveryCode', 'recovery_code': recovery_code})

    async def recover_password(self, recovery_code: str = None, new_password: str = None, new_hint: str = None) -> PasswordState:
        """
        description Recovers the 2-step verification password using a recovery code sent to an email address that was previously set up
        recovery_code Recovery code to check
        new_password New 2-step verification password of the user; may be empty to remove the password
        new_hint New password hint; may be empty
        """
        return await self._client.call_method('recoverPassword', {'@type': 'recoverPassword', 'recovery_code': recovery_code, 'new_password': new_password, 'new_hint': new_hint})

    async def reset_password(self) -> ResetPasswordResult:
        """
        description Removes 2-step verification password without previous password and access to recovery email address. The password can't be reset immediately and the request needs to be repeated after the specified time
        """
        return await self._client.call_method('resetPassword', {'@type': 'resetPassword'})

    async def cancel_password_reset(self) -> Ok:
        """
        description Cancels reset of 2-step verification password. The method can be called if passwordState.pending_reset_date > 0
        """
        return await self._client.call_method('cancelPasswordReset', {'@type': 'cancelPasswordReset'})

    async def create_temporary_password(self, password: str = None, valid_for: int = None) -> TemporaryPasswordState:
        """
        description Creates a new temporary password for processing payments @password The 2-step verification password of the current user @valid_for Time during which the temporary password will be valid, in seconds; must be between 60 and 86400
        """
        return await self._client.call_method('createTemporaryPassword', {'@type': 'createTemporaryPassword', 'password': password, 'valid_for': valid_for})

    async def get_temporary_password_state(self) -> TemporaryPasswordState:
        """
        description Returns information about the current temporary password
        """
        return await self._client.call_method('getTemporaryPasswordState', {'@type': 'getTemporaryPasswordState'})

    async def get_me(self) -> User:
        """
        description Returns the current user
        """
        return await self._client.call_method('getMe', {'@type': 'getMe'})

    async def get_user(self, user_id: int = None) -> User:
        """
        description Returns information about a user by their identifier. This is an offline method if the current user is not a bot @user_id User identifier
        """
        return await self._client.call_method('getUser', {'@type': 'getUser', 'user_id': user_id})

    async def get_user_full_info(self, user_id: int = None) -> UserFullInfo:
        """
        description Returns full information about a user by their identifier @user_id User identifier
        """
        return await self._client.call_method('getUserFullInfo', {'@type': 'getUserFullInfo', 'user_id': user_id})

    async def get_basic_group(self, basic_group_id: int = None) -> BasicGroup:
        """
        description Returns information about a basic group by its identifier. This is an offline method if the current user is not a bot @basic_group_id Basic group identifier
        """
        return await self._client.call_method('getBasicGroup', {'@type': 'getBasicGroup', 'basic_group_id': basic_group_id})

    async def get_basic_group_full_info(self, basic_group_id: int = None) -> BasicGroupFullInfo:
        """
        description Returns full information about a basic group by its identifier @basic_group_id Basic group identifier
        """
        return await self._client.call_method('getBasicGroupFullInfo', {'@type': 'getBasicGroupFullInfo', 'basic_group_id': basic_group_id})

    async def get_supergroup(self, supergroup_id: int = None) -> Supergroup:
        """
        description Returns information about a supergroup or a channel by its identifier. This is an offline method if the current user is not a bot @supergroup_id Supergroup or channel identifier
        """
        return await self._client.call_method('getSupergroup', {'@type': 'getSupergroup', 'supergroup_id': supergroup_id})

    async def get_supergroup_full_info(self, supergroup_id: int = None) -> SupergroupFullInfo:
        """
        description Returns full information about a supergroup or a channel by its identifier, cached for up to 1 minute @supergroup_id Supergroup or channel identifier
        """
        return await self._client.call_method('getSupergroupFullInfo', {'@type': 'getSupergroupFullInfo', 'supergroup_id': supergroup_id})

    async def get_secret_chat(self, secret_chat_id: int = None) -> SecretChat:
        """
        description Returns information about a secret chat by its identifier. This is an offline method @secret_chat_id Secret chat identifier
        """
        return await self._client.call_method('getSecretChat', {'@type': 'getSecretChat', 'secret_chat_id': secret_chat_id})

    async def get_chat(self, chat_id: int = None) -> Chat:
        """
        description Returns information about a chat by its identifier. This is an offline method if the current user is not a bot @chat_id Chat identifier
        """
        return await self._client.call_method('getChat', {'@type': 'getChat', 'chat_id': chat_id})

    async def get_message(self, chat_id: int = None, message_id: int = None) -> Message:
        """
        description Returns information about a message. Returns a 404 error if the message doesn't exist
        chat_id Identifier of the chat the message belongs to
        message_id Identifier of the message to get
        """
        return await self._client.call_method('getMessage', {'@type': 'getMessage', 'chat_id': chat_id, 'message_id': message_id})

    async def get_message_locally(self, chat_id: int = None, message_id: int = None) -> Message:
        """
        description Returns information about a message, if it is available without sending network request. Returns a 404 error if message isn't available locally. This is an offline method
        chat_id Identifier of the chat the message belongs to
        message_id Identifier of the message to get
        """
        return await self._client.call_method('getMessageLocally', {'@type': 'getMessageLocally', 'chat_id': chat_id, 'message_id': message_id})

    async def get_replied_message(self, chat_id: int = None, message_id: int = None) -> Message:
        """
        description Returns information about a non-bundled message that is replied by a given message. Also, returns the pinned message for messagePinMessage,
        chat_id Identifier of the chat the message belongs to
        message_id Identifier of the reply message
        """
        return await self._client.call_method('getRepliedMessage', {'@type': 'getRepliedMessage', 'chat_id': chat_id, 'message_id': message_id})

    async def get_chat_pinned_message(self, chat_id: int = None) -> Message:
        """
        description Returns information about a newest pinned message in the chat. Returns a 404 error if the message doesn't exist @chat_id Identifier of the chat the message belongs to
        """
        return await self._client.call_method('getChatPinnedMessage', {'@type': 'getChatPinnedMessage', 'chat_id': chat_id})

    async def get_callback_query_message(self, chat_id: int = None, message_id: int = None, callback_query_id: int = None) -> Message:
        """
        description Returns information about a message with the callback button that originated a callback query; for bots only @chat_id Identifier of the chat the message belongs to @message_id Message identifier @callback_query_id Identifier of the callback query
        """
        return await self._client.call_method('getCallbackQueryMessage', {'@type': 'getCallbackQueryMessage', 'chat_id': chat_id, 'message_id': message_id, 'callback_query_id': callback_query_id})

    async def get_messages(self, chat_id: int = None, message_ids: List[int] = None) -> Messages:
        """
        description Returns information about messages. If a message is not found, returns null on the corresponding position of the result @chat_id Identifier of the chat the messages belong to @message_ids Identifiers of the messages to get
        """
        return await self._client.call_method('getMessages', {'@type': 'getMessages', 'chat_id': chat_id, 'message_ids': message_ids})

    async def get_full_rich_message(self, chat_id: int = None, message_id: int = None) -> RichMessage:
        """
        description Returns the full version of a rich message @chat_id Identifier of the chat the messages belong to @message_id Identifier of the message
        """
        return await self._client.call_method('getFullRichMessage', {'@type': 'getFullRichMessage', 'chat_id': chat_id, 'message_id': message_id})

    async def get_message_properties(self, chat_id: int = None, message_id: int = None) -> MessageProperties:
        """
        description Returns properties of a message. This is an offline method @chat_id Chat identifier @message_id Identifier of the message
        """
        return await self._client.call_method('getMessageProperties', {'@type': 'getMessageProperties', 'chat_id': chat_id, 'message_id': message_id})

    async def get_poll_option_properties(self, chat_id: int = None, message_id: int = None, poll_option_id: str = None) -> PollOptionProperties:
        """
        description Returns properties of a poll option. This is an offline method
        chat_id Chat identifier
        message_id Identifier of the message
        poll_option_id Unique identifier of the answer option, which properties will be returned
        """
        return await self._client.call_method('getPollOptionProperties', {'@type': 'getPollOptionProperties', 'chat_id': chat_id, 'message_id': message_id, 'poll_option_id': poll_option_id})

    async def get_message_thread(self, chat_id: int = None, message_id: int = None) -> MessageThreadInfo:
        """
        description Returns information about a message thread. Can be used only if messageProperties.can_get_message_thread == true @chat_id Chat identifier @message_id Identifier of the message
        """
        return await self._client.call_method('getMessageThread', {'@type': 'getMessageThread', 'chat_id': chat_id, 'message_id': message_id})

    async def get_message_read_date(self, chat_id: int = None, message_id: int = None) -> MessageReadDate:
        """
        description Returns read date of a recent outgoing message in a private chat. The method can be called if messageProperties.can_get_read_date == true
        chat_id Chat identifier
        message_id Identifier of the message
        """
        return await self._client.call_method('getMessageReadDate', {'@type': 'getMessageReadDate', 'chat_id': chat_id, 'message_id': message_id})

    async def get_message_viewers(self, chat_id: int = None, message_id: int = None) -> MessageViewers:
        """
        description Returns viewers of a recent outgoing message in a basic group or a supergroup chat. For video notes and voice notes only users, opened content of the message, are returned. The method can be called if messageProperties.can_get_viewers == true
        chat_id Chat identifier
        message_id Identifier of the message
        """
        return await self._client.call_method('getMessageViewers', {'@type': 'getMessageViewers', 'chat_id': chat_id, 'message_id': message_id})

    async def get_message_author(self, chat_id: int = None, message_id: int = None) -> User:
        """
        description Returns information about actual author of a message sent on behalf of a channel. The method can be called if messageProperties.can_get_author == true
        chat_id Chat identifier
        message_id Identifier of the message
        """
        return await self._client.call_method('getMessageAuthor', {'@type': 'getMessageAuthor', 'chat_id': chat_id, 'message_id': message_id})

    async def get_file(self, file_id: int = None) -> File:
        """
        description Returns information about a file. This is an offline method @file_id Identifier of the file to get
        """
        return await self._client.call_method('getFile', {'@type': 'getFile', 'file_id': file_id})

    async def get_remote_file(self, remote_file_id: str = None, file_type: FileType = None) -> File:
        """
        description Returns information about a file by its remote identifier. This is an offline method. Can be used to register a URL as a file for further uploading, or sending as a message. Even if the request succeeds, the file can be used only if it is still accessible to the user.
        remote_file_id Remote identifier of the file to get
        file_type File type; pass null if unknown
        """
        return await self._client.call_method('getRemoteFile', {'@type': 'getRemoteFile', 'remote_file_id': remote_file_id, 'file_type': file_type})

    async def load_chats(self, chat_list: ChatList = None, limit: int = None) -> Ok:
        """
        description Loads more chats from a chat list. The loaded chats and their positions in the chat list will be sent through updates. Chats are sorted by the pair (chat.position.order, chat.id) in descending order. Returns a 404 error if all chats have been loaded
        chat_list The chat list in which to load chats; pass null to load chats from the main chat list
        limit The maximum number of chats to be loaded. For optimal performance, the number of loaded chats is chosen by TDLib and can be smaller than the specified limit, even if the end of the list is not reached
        """
        return await self._client.call_method('loadChats', {'@type': 'loadChats', 'chat_list': chat_list, 'limit': limit})

    async def get_chats(self, chat_list: ChatList = None, limit: int = None) -> Chats:
        """
        description Returns an ordered list of chats from the beginning of a chat list. For informational purposes only. Use loadChats and updates processing instead to maintain chat lists in a consistent state
        chat_list The chat list in which to return chats; pass null to get chats from the main chat list
        limit The maximum number of chats to be returned
        """
        return await self._client.call_method('getChats', {'@type': 'getChats', 'chat_list': chat_list, 'limit': limit})

    async def search_public_chat(self, username: str = None) -> Chat:
        """
        description Searches a public chat by its username. Currently, only private chats, supergroups and channels can be public. Returns the chat if found; otherwise, an error is returned @username Username to be resolved
        """
        return await self._client.call_method('searchPublicChat', {'@type': 'searchPublicChat', 'username': username})

    async def search_public_chats(self, query: str = None, type_filter: SearchChatTypeFilter = None) -> Chats:
        """
        description Searches public chats by looking for specified query in their username and title. Currently, only private chats, supergroups and channels can be public. Returns a meaningful number of results.
        query Query to search for
        type_filter Additional filter for type of the chats to be returned; pass null to search for chats of all types
        """
        return await self._client.call_method('searchPublicChats', {'@type': 'searchPublicChats', 'query': query, 'type_filter': type_filter})

    async def search_chats(self, query: str = None, type_filter: SearchChatTypeFilter = None, limit: int = None) -> Chats:
        """
        description Searches for the specified query in the title and username of already known chats. This is an offline method. Returns chats in the order seen in the main chat list
        query Query to search for. If the query is empty, returns up to 50 recently found chats
        type_filter Additional filter for type of the chats to be returned; pass null to search for chats of all types
        limit The maximum number of chats to be returned
        """
        return await self._client.call_method('searchChats', {'@type': 'searchChats', 'query': query, 'type_filter': type_filter, 'limit': limit})

    async def search_chats_on_server(self, query: str = None, type_filter: SearchChatTypeFilter = None, limit: int = None) -> Chats:
        """
        description Searches for the specified query in the title and username of already known chats via request to the server. Returns chats in the order seen in the main chat list
        query Query to search for
        type_filter Additional filter for type of the chats to be returned; pass null to search for chats of all types
        limit The maximum number of chats to be returned
        """
        return await self._client.call_method('searchChatsOnServer', {'@type': 'searchChatsOnServer', 'query': query, 'type_filter': type_filter, 'limit': limit})

    async def get_recommended_chats(self) -> Chats:
        """
        description Returns a list of channel chats recommended to the current user
        """
        return await self._client.call_method('getRecommendedChats', {'@type': 'getRecommendedChats'})

    async def get_chat_similar_chats(self, chat_id: int = None) -> Chats:
        """
        description Returns a list of chats similar to the given chat @chat_id Identifier of the target chat; must be an identifier of a channel chat
        """
        return await self._client.call_method('getChatSimilarChats', {'@type': 'getChatSimilarChats', 'chat_id': chat_id})

    async def get_chat_similar_chat_count(self, chat_id: int = None, return_local: bool = None) -> Count:
        """
        description Returns approximate number of chats similar to the given chat
        chat_id Identifier of the target chat; must be an identifier of a channel chat
        return_local Pass true to get the number of chats without sending network requests, or -1 if the number of chats is unknown locally
        """
        return await self._client.call_method('getChatSimilarChatCount', {'@type': 'getChatSimilarChatCount', 'chat_id': chat_id, 'return_local': return_local})

    async def open_chat_similar_chat(self, chat_id: int = None, opened_chat_id: int = None) -> Ok:
        """
        description Informs TDLib that a chat was opened from the list of similar chats. The method is independent of openChat and closeChat methods
        chat_id Identifier of the original chat, which similar chats were requested
        opened_chat_id Identifier of the opened chat
        """
        return await self._client.call_method('openChatSimilarChat', {'@type': 'openChatSimilarChat', 'chat_id': chat_id, 'opened_chat_id': opened_chat_id})

    async def get_bot_similar_bots(self, bot_user_id: int = None) -> Users:
        """
        description Returns a list of bots similar to the given bot @bot_user_id User identifier of the target bot
        """
        return await self._client.call_method('getBotSimilarBots', {'@type': 'getBotSimilarBots', 'bot_user_id': bot_user_id})

    async def get_bot_similar_bot_count(self, bot_user_id: int = None, return_local: bool = None) -> Count:
        """
        description Returns approximate number of bots similar to the given bot
        bot_user_id User identifier of the target bot
        return_local Pass true to get the number of bots without sending network requests, or -1 if the number of bots is unknown locally
        """
        return await self._client.call_method('getBotSimilarBotCount', {'@type': 'getBotSimilarBotCount', 'bot_user_id': bot_user_id, 'return_local': return_local})

    async def open_bot_similar_bot(self, bot_user_id: int = None, opened_bot_user_id: int = None) -> Ok:
        """
        description Informs TDLib that a bot was opened from the list of similar bots
        bot_user_id Identifier of the original bot, which similar bots were requested
        opened_bot_user_id Identifier of the opened bot
        """
        return await self._client.call_method('openBotSimilarBot', {'@type': 'openBotSimilarBot', 'bot_user_id': bot_user_id, 'opened_bot_user_id': opened_bot_user_id})

    async def get_top_chats(self, category: TopChatCategory = None, limit: int = None) -> Chats:
        """
        description Returns a list of frequently used chats @category Category of chats to be returned @limit The maximum number of chats to be returned; up to 30
        """
        return await self._client.call_method('getTopChats', {'@type': 'getTopChats', 'category': category, 'limit': limit})

    async def remove_top_chat(self, category: TopChatCategory = None, chat_id: int = None) -> Ok:
        """
        description Removes a chat from the list of frequently used chats. Supported only if the chat info database is enabled @category Category of frequently used chats @chat_id Chat identifier
        """
        return await self._client.call_method('removeTopChat', {'@type': 'removeTopChat', 'category': category, 'chat_id': chat_id})

    async def search_recently_found_chats(self, query: str = None, type_filter: SearchChatTypeFilter = None, limit: int = None) -> Chats:
        """
        description Searches for the specified query in the title and username of up to 50 recently found chats. This is an offline method
        query Query to search for
        type_filter Additional filter for type of the chats to be returned; pass null to search for chats of all types
        limit The maximum number of chats to be returned
        """
        return await self._client.call_method('searchRecentlyFoundChats', {'@type': 'searchRecentlyFoundChats', 'query': query, 'type_filter': type_filter, 'limit': limit})

    async def add_recently_found_chat(self, chat_id: int = None) -> Ok:
        """
        description Adds a chat to the list of recently found chats. The chat is added to the beginning of the list. If the chat is already in the list, it will be removed from the list first @chat_id Identifier of the chat to add
        """
        return await self._client.call_method('addRecentlyFoundChat', {'@type': 'addRecentlyFoundChat', 'chat_id': chat_id})

    async def remove_recently_found_chat(self, chat_id: int = None) -> Ok:
        """
        description Removes a chat from the list of recently found chats @chat_id Identifier of the chat to be removed
        """
        return await self._client.call_method('removeRecentlyFoundChat', {'@type': 'removeRecentlyFoundChat', 'chat_id': chat_id})

    async def clear_recently_found_chats(self) -> Ok:
        """
        description Clears the list of recently found chats
        """
        return await self._client.call_method('clearRecentlyFoundChats', {'@type': 'clearRecentlyFoundChats'})

    async def get_recently_opened_chats(self, limit: int = None) -> Chats:
        """
        description Returns recently opened chats. This is an offline method. Returns chats in the order of last opening @limit The maximum number of chats to be returned
        """
        return await self._client.call_method('getRecentlyOpenedChats', {'@type': 'getRecentlyOpenedChats', 'limit': limit})

    async def check_chat_username(self, chat_id: int = None, username: str = None) -> CheckChatUsernameResult:
        """
        description Checks whether a username can be set for a chat @chat_id Chat identifier; must be identifier of a supergroup chat, or a channel chat, or a private chat with self, or 0 if the chat is being created @username Username to be checked
        """
        return await self._client.call_method('checkChatUsername', {'@type': 'checkChatUsername', 'chat_id': chat_id, 'username': username})

    async def get_created_public_chats(self, type: PublicChatType = None) -> Chats:
        """
        description Returns a list of public chats of the specified type, owned by the user @type Type of the public chats to return
        """
        return await self._client.call_method('getCreatedPublicChats', {'@type': 'getCreatedPublicChats', 'type': type})

    async def check_created_public_chats_limit(self, type: PublicChatType = None) -> Ok:
        """
        description Checks whether the maximum number of owned public chats has been reached. Returns corresponding error if the limit was reached. The limit can be increased with Telegram Premium @type Type of the public chats, for which to check the limit
        """
        return await self._client.call_method('checkCreatedPublicChatsLimit', {'@type': 'checkCreatedPublicChatsLimit', 'type': type})

    async def get_suitable_discussion_chats(self) -> Chats:
        """
        description Returns a list of basic group and supergroup chats, which can be used as a discussion group for a channel. Returned basic group chats must be first upgraded to supergroups before they can be set as a discussion group.
        """
        return await self._client.call_method('getSuitableDiscussionChats', {'@type': 'getSuitableDiscussionChats'})

    async def get_inactive_supergroup_chats(self) -> Chats:
        """
        description Returns a list of recently inactive supergroups and channels. Can be used when user reaches limit on the number of joined supergroups and channels and receives the error "CHANNELS_TOO_MUCH". Also, the limit can be increased with Telegram Premium
        """
        return await self._client.call_method('getInactiveSupergroupChats', {'@type': 'getInactiveSupergroupChats'})

    async def get_suitable_personal_chats(self) -> Chats:
        """
        description Returns a list of channel chats, which can be used as a personal chat
        """
        return await self._client.call_method('getSuitablePersonalChats', {'@type': 'getSuitablePersonalChats'})

    async def load_direct_messages_chat_topics(self, chat_id: int = None, limit: int = None) -> Ok:
        """
        description Loads more topics in a channel direct messages chat administered by the current user. The loaded topics will be sent through updateDirectMessagesChatTopic.
        chat_id Chat identifier of the channel direct messages chat
        limit The maximum number of topics to be loaded. For optimal performance, the number of loaded topics is chosen by TDLib and can be smaller than the specified limit, even if the end of the list is not reached
        """
        return await self._client.call_method('loadDirectMessagesChatTopics', {'@type': 'loadDirectMessagesChatTopics', 'chat_id': chat_id, 'limit': limit})

    async def get_direct_messages_chat_topic(self, chat_id: int = None, topic_id: int = None) -> DirectMessagesChatTopic:
        """
        description Returns information about the topic in a channel direct messages chat administered by the current user
        chat_id Chat identifier of the channel direct messages chat
        topic_id Identifier of the topic to get
        """
        return await self._client.call_method('getDirectMessagesChatTopic', {'@type': 'getDirectMessagesChatTopic', 'chat_id': chat_id, 'topic_id': topic_id})

    async def get_direct_messages_chat_topic_history(self, chat_id: int = None, topic_id: int = None, from_message_id: int = None, offset: int = None, limit: int = None) -> Messages:
        """
        description Returns messages in the topic in a channel direct messages chat administered by the current user. The messages are returned in reverse chronological order (i.e., in order of decreasing message_id)
        chat_id Chat identifier of the channel direct messages chat
        topic_id Identifier of the topic which messages will be fetched
        from_message_id Identifier of the message starting from which messages must be fetched; use 0 to get results from the last message
        offset Specify 0 to get results from exactly the message from_message_id or a negative number from -99 to -1 to get additionally -offset newer messages
        limit The maximum number of messages to be returned; must be positive and can't be greater than 100. If the offset is negative, then the limit must be greater than or equal to -offset.
        """
        return await self._client.call_method('getDirectMessagesChatTopicHistory', {'@type': 'getDirectMessagesChatTopicHistory', 'chat_id': chat_id, 'topic_id': topic_id, 'from_message_id': from_message_id, 'offset': offset, 'limit': limit})

    async def get_direct_messages_chat_topic_message_by_date(self, chat_id: int = None, topic_id: int = None, date: int = None) -> Message:
        """
        description Returns the last message sent in the topic in a channel direct messages chat administered by the current user no later than the specified date
        chat_id Chat identifier of the channel direct messages chat
        topic_id Identifier of the topic which messages will be fetched
        date Point in time (Unix timestamp) relative to which to search for messages
        """
        return await self._client.call_method('getDirectMessagesChatTopicMessageByDate', {'@type': 'getDirectMessagesChatTopicMessageByDate', 'chat_id': chat_id, 'topic_id': topic_id, 'date': date})

    async def delete_direct_messages_chat_topic_history(self, chat_id: int = None, topic_id: int = None) -> Ok:
        """
        description Deletes all messages in the topic in a channel direct messages chat administered by the current user
        chat_id Chat identifier of the channel direct messages chat
        topic_id Identifier of the topic which messages will be deleted
        """
        return await self._client.call_method('deleteDirectMessagesChatTopicHistory', {'@type': 'deleteDirectMessagesChatTopicHistory', 'chat_id': chat_id, 'topic_id': topic_id})

    async def delete_direct_messages_chat_topic_messages_by_date(self, chat_id: int = None, topic_id: int = None, min_date: int = None, max_date: int = None) -> Ok:
        """
        description Deletes all messages between the specified dates in the topic in a channel direct messages chat administered by the current user. Messages sent in the last 30 seconds will not be deleted
        chat_id Chat identifier of the channel direct messages chat
        topic_id Identifier of the topic which messages will be deleted
        min_date The minimum date of the messages to delete
        max_date The maximum date of the messages to delete
        """
        return await self._client.call_method('deleteDirectMessagesChatTopicMessagesByDate', {'@type': 'deleteDirectMessagesChatTopicMessagesByDate', 'chat_id': chat_id, 'topic_id': topic_id, 'min_date': min_date, 'max_date': max_date})

    async def set_direct_messages_chat_topic_is_marked_as_unread(self, chat_id: int = None, topic_id: int = None, is_marked_as_unread: bool = None) -> Ok:
        """
        description Changes the marked as unread state of the topic in a channel direct messages chat administered by the current user
        chat_id Chat identifier of the channel direct messages chat
        topic_id Topic identifier
        is_marked_as_unread New value of is_marked_as_unread
        """
        return await self._client.call_method('setDirectMessagesChatTopicIsMarkedAsUnread', {'@type': 'setDirectMessagesChatTopicIsMarkedAsUnread', 'chat_id': chat_id, 'topic_id': topic_id, 'is_marked_as_unread': is_marked_as_unread})

    async def unpin_all_direct_messages_chat_topic_messages(self, chat_id: int = None, topic_id: int = None) -> Ok:
        """
        description Removes all pinned messages from the topic in a channel direct messages chat administered by the current user
        chat_id Identifier of the chat
        topic_id Topic identifier
        """
        return await self._client.call_method('unpinAllDirectMessagesChatTopicMessages', {'@type': 'unpinAllDirectMessagesChatTopicMessages', 'chat_id': chat_id, 'topic_id': topic_id})

    async def read_all_direct_messages_chat_topic_reactions(self, chat_id: int = None, topic_id: int = None) -> Ok:
        """
        description Removes all unread reactions in the topic in a channel direct messages chat administered by the current user
        chat_id Identifier of the chat
        topic_id Topic identifier
        """
        return await self._client.call_method('readAllDirectMessagesChatTopicReactions', {'@type': 'readAllDirectMessagesChatTopicReactions', 'chat_id': chat_id, 'topic_id': topic_id})

    async def get_direct_messages_chat_topic_revenue(self, chat_id: int = None, topic_id: int = None) -> StarCount:
        """
        description Returns the total number of Telegram Stars received by the channel chat for direct messages from the given topic
        chat_id Chat identifier of the channel direct messages chat administered by the current user
        topic_id Identifier of the topic
        """
        return await self._client.call_method('getDirectMessagesChatTopicRevenue', {'@type': 'getDirectMessagesChatTopicRevenue', 'chat_id': chat_id, 'topic_id': topic_id})

    async def toggle_direct_messages_chat_topic_can_send_unpaid_messages(self, chat_id: int = None, topic_id: int = None, can_send_unpaid_messages: bool = None, refund_payments: bool = None) -> Ok:
        """
        description Allows to send unpaid messages to the given topic of the channel direct messages chat administered by the current user
        chat_id Chat identifier
        topic_id Identifier of the topic
        can_send_unpaid_messages Pass true to allow unpaid messages; pass false to disallow unpaid messages
        refund_payments Pass true to refund the user previously paid messages
        """
        return await self._client.call_method('toggleDirectMessagesChatTopicCanSendUnpaidMessages', {'@type': 'toggleDirectMessagesChatTopicCanSendUnpaidMessages', 'chat_id': chat_id, 'topic_id': topic_id, 'can_send_unpaid_messages': can_send_unpaid_messages, 'refund_payments': refund_payments})

    async def load_saved_messages_topics(self, limit: int = None) -> Ok:
        """
        description Loads more Saved Messages topics. The loaded topics will be sent through updateSavedMessagesTopic. Topics are sorted by their topic.order in descending order. Returns a 404 error if all topics have been loaded
        limit The maximum number of topics to be loaded. For optimal performance, the number of loaded topics is chosen by TDLib and can be smaller than the specified limit, even if the end of the list is not reached
        """
        return await self._client.call_method('loadSavedMessagesTopics', {'@type': 'loadSavedMessagesTopics', 'limit': limit})

    async def get_saved_messages_topic_history(self, saved_messages_topic_id: int = None, from_message_id: int = None, offset: int = None, limit: int = None) -> Messages:
        """
        description Returns messages in a Saved Messages topic. The messages are returned in reverse chronological order (i.e., in order of decreasing message_id)
        saved_messages_topic_id Identifier of Saved Messages topic which messages will be fetched
        from_message_id Identifier of the message starting from which messages must be fetched; use 0 to get results from the last message
        offset Specify 0 to get results from exactly the message from_message_id or a negative number from -99 to -1 to get additionally -offset newer messages
        limit The maximum number of messages to be returned; must be positive and can't be greater than 100. If the offset is negative, then the limit must be greater than or equal to -offset.
        """
        return await self._client.call_method('getSavedMessagesTopicHistory', {'@type': 'getSavedMessagesTopicHistory', 'saved_messages_topic_id': saved_messages_topic_id, 'from_message_id': from_message_id, 'offset': offset, 'limit': limit})

    async def get_saved_messages_topic_message_by_date(self, saved_messages_topic_id: int = None, date: int = None) -> Message:
        """
        description Returns the last message sent in a Saved Messages topic no later than the specified date
        saved_messages_topic_id Identifier of Saved Messages topic which message will be returned
        date Point in time (Unix timestamp) relative to which to search for messages
        """
        return await self._client.call_method('getSavedMessagesTopicMessageByDate', {'@type': 'getSavedMessagesTopicMessageByDate', 'saved_messages_topic_id': saved_messages_topic_id, 'date': date})

    async def delete_saved_messages_topic_history(self, saved_messages_topic_id: int = None) -> Ok:
        """
        description Deletes all messages in a Saved Messages topic @saved_messages_topic_id Identifier of Saved Messages topic which messages will be deleted
        """
        return await self._client.call_method('deleteSavedMessagesTopicHistory', {'@type': 'deleteSavedMessagesTopicHistory', 'saved_messages_topic_id': saved_messages_topic_id})

    async def delete_saved_messages_topic_messages_by_date(self, saved_messages_topic_id: int = None, min_date: int = None, max_date: int = None) -> Ok:
        """
        description Deletes all messages between the specified dates in a Saved Messages topic. Messages sent in the last 30 seconds will not be deleted
        saved_messages_topic_id Identifier of Saved Messages topic which messages will be deleted
        min_date The minimum date of the messages to delete
        max_date The maximum date of the messages to delete
        """
        return await self._client.call_method('deleteSavedMessagesTopicMessagesByDate', {'@type': 'deleteSavedMessagesTopicMessagesByDate', 'saved_messages_topic_id': saved_messages_topic_id, 'min_date': min_date, 'max_date': max_date})

    async def toggle_saved_messages_topic_is_pinned(self, saved_messages_topic_id: int = None, is_pinned: bool = None) -> Ok:
        """
        description Changes the pinned state of a Saved Messages topic. There can be up to getOption("pinned_saved_messages_topic_count_max") pinned topics. The limit can be increased with Telegram Premium
        saved_messages_topic_id Identifier of Saved Messages topic to pin or unpin
        is_pinned Pass true to pin the topic; pass false to unpin it
        """
        return await self._client.call_method('toggleSavedMessagesTopicIsPinned', {'@type': 'toggleSavedMessagesTopicIsPinned', 'saved_messages_topic_id': saved_messages_topic_id, 'is_pinned': is_pinned})

    async def set_pinned_saved_messages_topics(self, saved_messages_topic_ids: List[int] = None) -> Ok:
        """
        description Changes the order of pinned Saved Messages topics @saved_messages_topic_ids Identifiers of the new pinned Saved Messages topics
        """
        return await self._client.call_method('setPinnedSavedMessagesTopics', {'@type': 'setPinnedSavedMessagesTopics', 'saved_messages_topic_ids': saved_messages_topic_ids})

    async def get_groups_in_common(self, user_id: int = None, offset_chat_id: int = None, limit: int = None) -> Chats:
        """
        description Returns a list of common group chats with a given user. Chats are sorted by their type and creation date
        user_id User identifier
        offset_chat_id Chat identifier starting from which to return chats; use 0 for the first request
        limit The maximum number of chats to be returned; up to 100
        """
        return await self._client.call_method('getGroupsInCommon', {'@type': 'getGroupsInCommon', 'user_id': user_id, 'offset_chat_id': offset_chat_id, 'limit': limit})

    async def get_chat_history(self, chat_id: int = None, from_message_id: int = None, offset: int = None, limit: int = None, only_local: bool = None) -> Messages:
        """
        description Returns messages in a chat. The messages are returned in reverse chronological order (i.e., in order of decreasing message_id).
        chat_id Chat identifier
        from_message_id Identifier of the message starting from which history must be fetched; use 0 to get results from the last message
        offset Specify 0 to get results from exactly the message from_message_id or a negative number from -99 to -1 to get additionally -offset newer messages
        limit The maximum number of messages to be returned; must be positive and can't be greater than 100. If the offset is negative, then the limit must be greater than or equal to -offset.
        only_local Pass true to get only messages that are available without sending network requests
        """
        return await self._client.call_method('getChatHistory', {'@type': 'getChatHistory', 'chat_id': chat_id, 'from_message_id': from_message_id, 'offset': offset, 'limit': limit, 'only_local': only_local})

    async def get_message_thread_history(self, chat_id: int = None, message_id: int = None, from_message_id: int = None, offset: int = None, limit: int = None) -> Messages:
        """
        description Returns messages in a message thread of a message. Can be used only if messageProperties.can_get_message_thread == true. Message thread of a channel message is in the channel's linked supergroup.
        chat_id Chat identifier
        message_id Message identifier, which thread history needs to be returned
        from_message_id Identifier of the message starting from which history must be fetched; use 0 to get results from the last message
        offset Specify 0 to get results from exactly the message from_message_id or a negative number from -99 to -1 to get additionally -offset newer messages
        limit The maximum number of messages to be returned; must be positive and can't be greater than 100. If the offset is negative, then the limit must be greater than or equal to -offset.
        """
        return await self._client.call_method('getMessageThreadHistory', {'@type': 'getMessageThreadHistory', 'chat_id': chat_id, 'message_id': message_id, 'from_message_id': from_message_id, 'offset': offset, 'limit': limit})

    async def delete_chat_history(self, chat_id: int = None, remove_from_chat_list: bool = None, revoke: bool = None) -> Ok:
        """
        description Deletes all messages in the chat. Use chat.can_be_deleted_only_for_self and chat.can_be_deleted_for_all_users fields to find whether and how the method can be applied to the chat
        chat_id Chat identifier
        remove_from_chat_list Pass true to remove the chat from all chat lists
        revoke Pass true to delete chat history for all users
        """
        return await self._client.call_method('deleteChatHistory', {'@type': 'deleteChatHistory', 'chat_id': chat_id, 'remove_from_chat_list': remove_from_chat_list, 'revoke': revoke})

    async def delete_chat(self, chat_id: int = None) -> Ok:
        """
        description Deletes a chat along with all messages in the corresponding chat for all chat members. For group chats this will release the usernames and remove all members.
        chat_id Chat identifier
        """
        return await self._client.call_method('deleteChat', {'@type': 'deleteChat', 'chat_id': chat_id})

    async def search_chat_messages(self, chat_id: int = None, topic_id: MessageTopic = None, query: str = None, sender_id: MessageSender = None, from_message_id: int = None, offset: int = None, limit: int = None, filter: SearchMessagesFilter = None) -> FoundChatMessages:
        """
        description Searches for messages with given words in the chat. Returns the results in reverse chronological order, i.e. in order of decreasing message_id. Cannot be used in secret chats with a non-empty query
        chat_id Identifier of the chat in which to search messages
        topic_id Pass topic identifier to search messages only in specific topic; pass null to search for messages in all topics
        query Query to search for
        sender_id Identifier of the sender of messages to search for; pass null to search for messages from any sender. Not supported in secret chats
        from_message_id Identifier of the message starting from which history must be fetched; use 0 to get results from the last message
        offset Specify 0 to get results from exactly the message from_message_id or a negative number to get the specified message and some newer messages
        limit The maximum number of messages to be returned; must be positive and can't be greater than 100. If the offset is negative, then the limit must be greater than -offset.
        filter Additional filter for messages to search; pass null to search for all messages
        """
        return await self._client.call_method('searchChatMessages', {'@type': 'searchChatMessages', 'chat_id': chat_id, 'topic_id': topic_id, 'query': query, 'sender_id': sender_id, 'from_message_id': from_message_id, 'offset': offset, 'limit': limit, 'filter': filter})

    async def search_messages(self, chat_list: ChatList = None, query: str = None, offset: str = None, limit: int = None, filter: SearchMessagesFilter = None, chat_type_filter: SearchMessagesChatTypeFilter = None, min_date: int = None, max_date: int = None) -> FoundMessages:
        """
        description Searches for messages in all chats except secret chats. Returns the results in reverse chronological order (i.e., in order of decreasing (date, chat_id, message_id)).
        chat_list Chat list in which to search messages; pass null to search in all chats regardless of their chat list. Only Main and Archive chat lists are supported
        query Query to search for
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of messages to be returned; up to 100. For optimal performance, the number of returned messages is chosen by TDLib and can be smaller than the specified limit
        filter Additional filter for messages to search; pass null to search for all messages. Filters searchMessagesFilterMention, searchMessagesFilterUnreadMention, searchMessagesFilterUnreadReaction,
        chat_type_filter Additional filter for type of the chat of the searched messages; pass null to search for messages in all chats
        min_date If not 0, the minimum date of the messages to return
        max_date If not 0, the maximum date of the messages to return
        """
        return await self._client.call_method('searchMessages', {'@type': 'searchMessages', 'chat_list': chat_list, 'query': query, 'offset': offset, 'limit': limit, 'filter': filter, 'chat_type_filter': chat_type_filter, 'min_date': min_date, 'max_date': max_date})

    async def search_secret_messages(self, chat_id: int = None, query: str = None, offset: str = None, limit: int = None, filter: SearchMessagesFilter = None) -> FoundMessages:
        """
        description Searches for messages in secret chats. Returns the results in reverse chronological order. For optimal performance, the number of returned messages is chosen by TDLib
        chat_id Identifier of the chat in which to search. Specify 0 to search in all secret chats
        query Query to search for. If empty, searchChatMessages must be used instead
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of messages to be returned; up to 100. For optimal performance, the number of returned messages is chosen by TDLib and can be smaller than the specified limit
        filter Additional filter for messages to search; pass null to search for all messages
        """
        return await self._client.call_method('searchSecretMessages', {'@type': 'searchSecretMessages', 'chat_id': chat_id, 'query': query, 'offset': offset, 'limit': limit, 'filter': filter})

    async def search_saved_messages(self, saved_messages_topic_id: int = None, tag: ReactionType = None, query: str = None, from_message_id: int = None, offset: int = None, limit: int = None) -> FoundChatMessages:
        """
        description Searches for messages tagged by the given reaction and with the given words in the Saved Messages chat; for Telegram Premium users only.
        saved_messages_topic_id If not 0, only messages in the specified Saved Messages topic will be considered; pass 0 to consider all messages
        tag Tag to search for; pass null to return all suitable messages
        query Query to search for
        from_message_id Identifier of the message starting from which messages must be fetched; use 0 to get results from the last message
        offset Specify 0 to get results from exactly the message from_message_id or a negative number to get the specified message and some newer messages
        limit The maximum number of messages to be returned; must be positive and can't be greater than 100. If the offset is negative, then the limit must be greater than -offset.
        """
        return await self._client.call_method('searchSavedMessages', {'@type': 'searchSavedMessages', 'saved_messages_topic_id': saved_messages_topic_id, 'tag': tag, 'query': query, 'from_message_id': from_message_id, 'offset': offset, 'limit': limit})

    async def search_call_messages(self, offset: str = None, limit: int = None, only_missed: bool = None) -> FoundMessages:
        """
        description Searches for call and group call messages. Returns the results in reverse chronological order (i.e., in order of decreasing message_id). For optimal performance, the number of returned messages is chosen by TDLib
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of messages to be returned; up to 100. For optimal performance, the number of returned messages is chosen by TDLib and can be smaller than the specified limit
        only_missed Pass true to search only for messages with missed/declined calls
        """
        return await self._client.call_method('searchCallMessages', {'@type': 'searchCallMessages', 'offset': offset, 'limit': limit, 'only_missed': only_missed})

    async def search_outgoing_document_messages(self, query: str = None, limit: int = None) -> FoundMessages:
        """
        description Searches for outgoing messages with content of the type messageDocument in all chats except secret chats. Returns the results in reverse chronological order
        query Query to search for in document file name and message caption
        limit The maximum number of messages to be returned; up to 100
        """
        return await self._client.call_method('searchOutgoingDocumentMessages', {'@type': 'searchOutgoingDocumentMessages', 'query': query, 'limit': limit})

    async def get_public_post_search_limits(self, query: str = None) -> PublicPostSearchLimits:
        """
        description Checks public post search limits without actually performing the search @query Query that will be searched for
        """
        return await self._client.call_method('getPublicPostSearchLimits', {'@type': 'getPublicPostSearchLimits', 'query': query})

    async def search_public_posts(self, query: str = None, offset: str = None, limit: int = None, star_count: int = None) -> FoundPublicPosts:
        """
        description Searches for public channel posts using the given query. For optimal performance, the number of returned messages is chosen by TDLib and can be smaller than the specified limit
        query Query to search for
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of messages to be returned; up to 100. For optimal performance, the number of returned messages is chosen by TDLib and can be smaller than the specified limit
        star_count The Telegram Star amount the user agreed to pay for the search; pass 0 for free searches
        """
        return await self._client.call_method('searchPublicPosts', {'@type': 'searchPublicPosts', 'query': query, 'offset': offset, 'limit': limit, 'star_count': star_count})

    async def search_public_messages_by_tag(self, tag: str = None, offset: str = None, limit: int = None) -> FoundMessages:
        """
        description Searches for public channel posts containing the given hashtag or cashtag. For optimal performance, the number of returned messages is chosen by TDLib and can be smaller than the specified limit
        tag Hashtag or cashtag to search for
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of messages to be returned; up to 100. For optimal performance, the number of returned messages is chosen by TDLib and can be smaller than the specified limit
        """
        return await self._client.call_method('searchPublicMessagesByTag', {'@type': 'searchPublicMessagesByTag', 'tag': tag, 'offset': offset, 'limit': limit})

    async def search_public_stories_by_tag(self, story_poster_chat_id: int = None, tag: str = None, offset: str = None, limit: int = None) -> FoundStories:
        """
        description Searches for public stories containing the given hashtag or cashtag. For optimal performance, the number of returned stories is chosen by TDLib and can be smaller than the specified limit
        story_poster_chat_id Identifier of the chat that posted the stories to search for; pass 0 to search stories in all chats
        tag Hashtag or cashtag to search for
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of stories to be returned; up to 100. For optimal performance, the number of returned stories is chosen by TDLib and can be smaller than the specified limit
        """
        return await self._client.call_method('searchPublicStoriesByTag', {'@type': 'searchPublicStoriesByTag', 'story_poster_chat_id': story_poster_chat_id, 'tag': tag, 'offset': offset, 'limit': limit})

    async def search_public_stories_by_location(self, address: locationAddress = None, offset: str = None, limit: int = None) -> FoundStories:
        """
        description Searches for public stories by the given address location. For optimal performance, the number of returned stories is chosen by TDLib and can be smaller than the specified limit
        address Address of the location
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of stories to be returned; up to 100. For optimal performance, the number of returned stories is chosen by TDLib and can be smaller than the specified limit
        """
        return await self._client.call_method('searchPublicStoriesByLocation', {'@type': 'searchPublicStoriesByLocation', 'address': address, 'offset': offset, 'limit': limit})

    async def search_public_stories_by_venue(self, venue_provider: str = None, venue_id: str = None, offset: str = None, limit: int = None) -> FoundStories:
        """
        description Searches for public stories from the given venue. For optimal performance, the number of returned stories is chosen by TDLib and can be smaller than the specified limit
        venue_provider Provider of the venue
        venue_id Identifier of the venue in the provider database
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of stories to be returned; up to 100. For optimal performance, the number of returned stories is chosen by TDLib and can be smaller than the specified limit
        """
        return await self._client.call_method('searchPublicStoriesByVenue', {'@type': 'searchPublicStoriesByVenue', 'venue_provider': venue_provider, 'venue_id': venue_id, 'offset': offset, 'limit': limit})

    async def get_searched_for_tags(self, tag_prefix: str = None, limit: int = None) -> Hashtags:
        """
        description Returns recently searched for hashtags or cashtags by their prefix @tag_prefix Prefix of hashtags or cashtags to return @limit The maximum number of items to be returned
        """
        return await self._client.call_method('getSearchedForTags', {'@type': 'getSearchedForTags', 'tag_prefix': tag_prefix, 'limit': limit})

    async def remove_searched_for_tag(self, tag: str = None) -> Ok:
        """
        description Removes a hashtag or a cashtag from the list of recently searched for hashtags or cashtags @tag Hashtag or cashtag to delete
        """
        return await self._client.call_method('removeSearchedForTag', {'@type': 'removeSearchedForTag', 'tag': tag})

    async def clear_searched_for_tags(self, clear_cashtags: bool = None) -> Ok:
        """
        description Clears the list of recently searched for hashtags or cashtags @clear_cashtags Pass true to clear the list of recently searched for cashtags; otherwise, the list of recently searched for hashtags will be cleared
        """
        return await self._client.call_method('clearSearchedForTags', {'@type': 'clearSearchedForTags', 'clear_cashtags': clear_cashtags})

    async def delete_all_call_messages(self, revoke: bool = None) -> Ok:
        """
        description Deletes all call messages @revoke Pass true to delete the messages for all users
        """
        return await self._client.call_method('deleteAllCallMessages', {'@type': 'deleteAllCallMessages', 'revoke': revoke})

    async def search_chat_recent_location_messages(self, chat_id: int = None, limit: int = None) -> Messages:
        """
        description Returns information about the recent live locations of chat members that were sent to the chat. Returns at most one live location message per user @chat_id Chat identifier @limit The maximum number of messages to be returned
        """
        return await self._client.call_method('searchChatRecentLocationMessages', {'@type': 'searchChatRecentLocationMessages', 'chat_id': chat_id, 'limit': limit})

    async def get_chat_message_by_date(self, chat_id: int = None, date: int = None) -> Message:
        """
        description Returns the last message sent in a chat no later than the specified date. Returns a 404 error if such message doesn't exist
        chat_id Chat identifier
        date Point in time (Unix timestamp) relative to which to search for messages
        """
        return await self._client.call_method('getChatMessageByDate', {'@type': 'getChatMessageByDate', 'chat_id': chat_id, 'date': date})

    async def get_chat_sparse_message_positions(self, chat_id: int = None, filter: SearchMessagesFilter = None, from_message_id: int = None, limit: int = None, saved_messages_topic_id: int = None) -> MessagePositions:
        """
        description Returns sparse positions of messages of the specified type in the chat to be used for Shared Media scroll implementation. Returns the results in reverse chronological order (i.e., in order of decreasing message_id).
        chat_id Identifier of the chat in which to return information about message positions
        filter Filter for message content. Filters searchMessagesFilterEmpty, searchMessagesFilterMention, searchMessagesFilterUnreadMention, searchMessagesFilterUnreadReaction,
        from_message_id The message identifier from which to return information about message positions
        limit The expected number of message positions to be returned; 50-2000. A smaller number of positions can be returned, if there are not enough appropriate messages
        saved_messages_topic_id If not 0, only messages in the specified Saved Messages topic will be considered; pass 0 to consider all messages, or for chats other than Saved Messages
        """
        return await self._client.call_method('getChatSparseMessagePositions', {'@type': 'getChatSparseMessagePositions', 'chat_id': chat_id, 'filter': filter, 'from_message_id': from_message_id, 'limit': limit, 'saved_messages_topic_id': saved_messages_topic_id})

    async def get_chat_message_calendar(self, chat_id: int = None, topic_id: MessageTopic = None, filter: SearchMessagesFilter = None, from_message_id: int = None) -> MessageCalendar:
        """
        description Returns information about the next messages of the specified type in the chat split by days. Returns the results in reverse chronological order. Can return partial result for the last returned day. Behavior of this method depends on the value of the option "utc_time_offset"
        chat_id Identifier of the chat in which to return information about messages
        topic_id Pass topic identifier to get the result only in specific topic; pass null to get the result in all topics; forum topics and message threads aren't supported
        filter Filter for message content. Filters searchMessagesFilterEmpty, searchMessagesFilterMention, searchMessagesFilterUnreadMention, searchMessagesFilterUnreadReaction,
        from_message_id The message identifier from which to return information about messages; use 0 to get results from the last message
        """
        return await self._client.call_method('getChatMessageCalendar', {'@type': 'getChatMessageCalendar', 'chat_id': chat_id, 'topic_id': topic_id, 'filter': filter, 'from_message_id': from_message_id})

    async def get_chat_message_count(self, chat_id: int = None, topic_id: MessageTopic = None, filter: SearchMessagesFilter = None, return_local: bool = None) -> Count:
        """
        description Returns approximate number of messages of the specified type in the chat or its topic
        chat_id Identifier of the chat in which to count messages
        topic_id Pass topic identifier to get number of messages only in specific topic; pass null to get number of messages in all topics; message threads aren't supported
        filter Filter for message content; searchMessagesFilterEmpty is unsupported in this function
        return_local Pass true to get the number of messages without sending network requests, or -1 if the number of messages is unknown locally
        """
        return await self._client.call_method('getChatMessageCount', {'@type': 'getChatMessageCount', 'chat_id': chat_id, 'topic_id': topic_id, 'filter': filter, 'return_local': return_local})

    async def get_chat_message_position(self, chat_id: int = None, topic_id: MessageTopic = None, filter: SearchMessagesFilter = None, message_id: int = None) -> Count:
        """
        description Returns approximate 1-based position of a message among messages, which can be found by the specified filter in the chat and topic. Cannot be used in secret chats
        chat_id Identifier of the chat in which to find message position
        topic_id Pass topic identifier to get position among messages only in specific topic; pass null to get position among all chat messages; message threads aren't supported
        filter Filter for message content; searchMessagesFilterEmpty, searchMessagesFilterUnreadMention, searchMessagesFilterUnreadReaction, searchMessagesFilterUnreadPollVote,
        message_id Message identifier
        """
        return await self._client.call_method('getChatMessagePosition', {'@type': 'getChatMessagePosition', 'chat_id': chat_id, 'topic_id': topic_id, 'filter': filter, 'message_id': message_id})

    async def get_chat_scheduled_messages(self, chat_id: int = None) -> Messages:
        """
        description Returns all scheduled messages in a chat. The messages are returned in reverse chronological order (i.e., in order of decreasing message_id) @chat_id Chat identifier
        """
        return await self._client.call_method('getChatScheduledMessages', {'@type': 'getChatScheduledMessages', 'chat_id': chat_id})

    async def get_chat_sponsored_messages(self, chat_id: int = None) -> SponsoredMessages:
        """
        description Returns sponsored messages to be shown in a chat; for channel chats and chats with bots only @chat_id Identifier of the chat
        """
        return await self._client.call_method('getChatSponsoredMessages', {'@type': 'getChatSponsoredMessages', 'chat_id': chat_id})

    async def click_chat_sponsored_message(self, chat_id: int = None, message_id: int = None, is_media_click: bool = None, from_fullscreen: bool = None) -> Ok:
        """
        description Informs TDLib that the user opened the sponsored chat via the button, the name, the chat photo, a mention in the sponsored message text, or the media in the sponsored message
        chat_id Chat identifier of the sponsored message
        message_id Identifier of the sponsored message
        is_media_click Pass true if the media was clicked in the sponsored message
        from_fullscreen Pass true if the user expanded the video from the sponsored message fullscreen before the click
        """
        return await self._client.call_method('clickChatSponsoredMessage', {'@type': 'clickChatSponsoredMessage', 'chat_id': chat_id, 'message_id': message_id, 'is_media_click': is_media_click, 'from_fullscreen': from_fullscreen})

    async def report_chat_sponsored_message(self, chat_id: int = None, message_id: int = None, option_id: bytes = None) -> ReportSponsoredResult:
        """
        description Reports a sponsored message to Telegram moderators
        chat_id Chat identifier of the sponsored message
        message_id Identifier of the sponsored message
        option_id Option identifier chosen by the user; leave empty for the initial request
        """
        return await self._client.call_method('reportChatSponsoredMessage', {'@type': 'reportChatSponsoredMessage', 'chat_id': chat_id, 'message_id': message_id, 'option_id': option_id})

    async def get_search_sponsored_chats(self, query: str = None) -> SponsoredChats:
        """
        description Returns sponsored chats to be shown in the search results @query Query the user searches for
        """
        return await self._client.call_method('getSearchSponsoredChats', {'@type': 'getSearchSponsoredChats', 'query': query})

    async def view_sponsored_chat(self, sponsored_chat_unique_id: int = None) -> Ok:
        """
        description Informs TDLib that the user fully viewed a sponsored chat @sponsored_chat_unique_id Unique identifier of the sponsored chat
        """
        return await self._client.call_method('viewSponsoredChat', {'@type': 'viewSponsoredChat', 'sponsored_chat_unique_id': sponsored_chat_unique_id})

    async def open_sponsored_chat(self, sponsored_chat_unique_id: int = None) -> Ok:
        """
        description Informs TDLib that the user opened a sponsored chat @sponsored_chat_unique_id Unique identifier of the sponsored chat
        """
        return await self._client.call_method('openSponsoredChat', {'@type': 'openSponsoredChat', 'sponsored_chat_unique_id': sponsored_chat_unique_id})

    async def report_sponsored_chat(self, sponsored_chat_unique_id: int = None, option_id: bytes = None) -> ReportSponsoredResult:
        """
        description Reports a sponsored chat to Telegram moderators
        sponsored_chat_unique_id Unique identifier of the sponsored chat
        option_id Option identifier chosen by the user; leave empty for the initial request
        """
        return await self._client.call_method('reportSponsoredChat', {'@type': 'reportSponsoredChat', 'sponsored_chat_unique_id': sponsored_chat_unique_id, 'option_id': option_id})

    async def get_video_message_advertisements(self, chat_id: int = None, message_id: int = None) -> VideoMessageAdvertisements:
        """
        description Returns advertisements to be shown while a video from a message is watched. Available only if messageProperties.can_get_video_advertisements
        chat_id Identifier of the chat with the message
        message_id Identifier of the message
        """
        return await self._client.call_method('getVideoMessageAdvertisements', {'@type': 'getVideoMessageAdvertisements', 'chat_id': chat_id, 'message_id': message_id})

    async def view_video_message_advertisement(self, advertisement_unique_id: int = None) -> Ok:
        """
        description Informs TDLib that the user viewed a video message advertisement @advertisement_unique_id Unique identifier of the advertisement
        """
        return await self._client.call_method('viewVideoMessageAdvertisement', {'@type': 'viewVideoMessageAdvertisement', 'advertisement_unique_id': advertisement_unique_id})

    async def click_video_message_advertisement(self, advertisement_unique_id: int = None) -> Ok:
        """
        description Informs TDLib that the user clicked a video message advertisement @advertisement_unique_id Unique identifier of the advertisement
        """
        return await self._client.call_method('clickVideoMessageAdvertisement', {'@type': 'clickVideoMessageAdvertisement', 'advertisement_unique_id': advertisement_unique_id})

    async def report_video_message_advertisement(self, advertisement_unique_id: int = None, option_id: bytes = None) -> ReportSponsoredResult:
        """
        description Reports a video message advertisement to Telegram moderators
        advertisement_unique_id Unique identifier of the advertisement
        option_id Option identifier chosen by the user; leave empty for the initial request
        """
        return await self._client.call_method('reportVideoMessageAdvertisement', {'@type': 'reportVideoMessageAdvertisement', 'advertisement_unique_id': advertisement_unique_id, 'option_id': option_id})

    async def remove_notification(self, notification_group_id: int = None, notification_id: int = None) -> Ok:
        """
        description Removes an active notification from notification list. Needs to be called only if the notification is removed by the current user @notification_group_id Identifier of notification group to which the notification belongs @notification_id Identifier of removed notification
        """
        return await self._client.call_method('removeNotification', {'@type': 'removeNotification', 'notification_group_id': notification_group_id, 'notification_id': notification_id})

    async def remove_notification_group(self, notification_group_id: int = None, max_notification_id: int = None) -> Ok:
        """
        description Removes a group of active notifications. Needs to be called only if the notification group is removed by the current user @notification_group_id Notification group identifier @max_notification_id The maximum identifier of removed notifications
        """
        return await self._client.call_method('removeNotificationGroup', {'@type': 'removeNotificationGroup', 'notification_group_id': notification_group_id, 'max_notification_id': max_notification_id})

    async def get_message_link(self, chat_id: int = None, message_id: int = None, media_timestamp: int = None, checklist_task_id: int = None, poll_option_id: str = None, for_album: bool = None, in_message_thread: bool = None) -> MessageLink:
        """
        description Returns an HTTPS link to a message in a chat. Available only if messageProperties.can_get_link, or if messageProperties.can_get_media_timestamp_links and a media timestamp link is generated. This is an offline method
        chat_id Identifier of the chat to which the message belongs
        message_id Identifier of the message
        media_timestamp If not 0, timestamp from which the video/audio/video note/voice note/story playing must start, in seconds. The media can be in the message content or in its link preview
        checklist_task_id If not 0, identifier of the checklist task in the message to be linked
        poll_option_id If not empty, identifier of the poll option in the message to be linked
        for_album Pass true to create a link for the whole media album
        in_message_thread Pass true to create a link to the message as a channel post comment, in a message thread, or a forum topic
        """
        return await self._client.call_method('getMessageLink', {'@type': 'getMessageLink', 'chat_id': chat_id, 'message_id': message_id, 'media_timestamp': media_timestamp, 'checklist_task_id': checklist_task_id, 'poll_option_id': poll_option_id, 'for_album': for_album, 'in_message_thread': in_message_thread})

    async def get_message_embedding_code(self, chat_id: int = None, message_id: int = None, for_album: bool = None) -> Text:
        """
        description Returns an HTML code for embedding the message. Available only if messageProperties.can_get_embedding_code
        chat_id Identifier of the chat to which the message belongs
        message_id Identifier of the message
        for_album Pass true to return an HTML code for embedding of the whole media album
        """
        return await self._client.call_method('getMessageEmbeddingCode', {'@type': 'getMessageEmbeddingCode', 'chat_id': chat_id, 'message_id': message_id, 'for_album': for_album})

    async def get_message_link_info(self, url: str = None) -> MessageLinkInfo:
        """
        description Returns information about a public or private message link. Can be called for any internal link of the type internalLinkTypeMessage @url The message link
        """
        return await self._client.call_method('getMessageLinkInfo', {'@type': 'getMessageLinkInfo', 'url': url})

    async def create_text_composition_style(self, title: str = None, custom_emoji_id: int = None, prompt: str = None, show_creator: bool = None) -> TextCompositionStyle:
        """
        description Creates a custom text composition style. May return an error with a message "TONES_SAVED_TOO_MANY" if the maximum number of added custom styles has been reached
        title Title of the style; 1-getOption("text_composition_style_title_length_max") characters
        custom_emoji_id Identifier of the custom emoji corresponding to the style
        prompt Prompt that will be used for text composition; 1-getOption("text_composition_style_prompt_length_max") characters
        show_creator Pass true if the current user must be shown as the creator of the style
        """
        return await self._client.call_method('createTextCompositionStyle', {'@type': 'createTextCompositionStyle', 'title': title, 'custom_emoji_id': custom_emoji_id, 'prompt': prompt, 'show_creator': show_creator})

    async def edit_text_composition_style(self, name: str = None, title: str = None, custom_emoji_id: int = None, prompt: str = None, show_creator: bool = None) -> TextCompositionStyle:
        """
        description Edits a custom text composition style that was created by the current user
        name Name of the style
        title Title of the style; 1-getOption("text_composition_style_title_length_max") characters
        custom_emoji_id Identifier of the custom emoji corresponding to the style
        prompt Prompt that will be used for text composition; 1-getOption("text_composition_style_prompt_length_max") characters
        show_creator Pass true if the current user must be shown as the creator of the style
        """
        return await self._client.call_method('editTextCompositionStyle', {'@type': 'editTextCompositionStyle', 'name': name, 'title': title, 'custom_emoji_id': custom_emoji_id, 'prompt': prompt, 'show_creator': show_creator})

    async def delete_text_composition_style(self, name: str = None) -> Ok:
        """
        description Deletes a custom text composition style that was created by the current user
        name Name of the style
        """
        return await self._client.call_method('deleteTextCompositionStyle', {'@type': 'deleteTextCompositionStyle', 'name': name})

    async def search_text_composition_style(self, name: str = None) -> TextCompositionStyle:
        """
        description Searches a custom text composition style by its name @name Name of the style
        """
        return await self._client.call_method('searchTextCompositionStyle', {'@type': 'searchTextCompositionStyle', 'name': name})

    async def get_text_composition_style_example(self, name: str = None, example_number: int = None) -> TextCompositionStyleExample:
        """
        description Returns an example of usage of a custom text composition style
        name Name of the style
        example_number 0-based unique number of the requested example; must be non-negative and less than getOption("text_composition_style_example_count")
        """
        return await self._client.call_method('getTextCompositionStyleExample', {'@type': 'getTextCompositionStyleExample', 'name': name, 'example_number': example_number})

    async def add_text_composition_style(self, name: str = None) -> Ok:
        """
        description Adds a custom text composition style to the list of used by the user styles. May return an error with a message "TONES_SAVED_TOO_MANY" if the maximum number of added custom styles has been reached
        name Name of the style
        """
        return await self._client.call_method('addTextCompositionStyle', {'@type': 'addTextCompositionStyle', 'name': name})

    async def remove_text_composition_style(self, name: str = None) -> Ok:
        """
        description Removes a custom text composition style from the list of used by the user styles. If the style was created by the current user, then it can only be deleted
        name Name of the style
        """
        return await self._client.call_method('removeTextCompositionStyle', {'@type': 'removeTextCompositionStyle', 'name': name})

    async def translate_text(self, text: formattedText = None, to_language_code: str = None, tone: str = None) -> FormattedText:
        """
        description Translates a text to the given language; must not be used in secret chats. If the current user is a Telegram Premium user, then text formatting is preserved
        text Text to translate
        to_language_code Language code of the language to which the message is translated. Must be one of
        tone Tone of the translation; must be one of "", "formal", "neutral", "casual"; defaults to "neutral"
        """
        return await self._client.call_method('translateText', {'@type': 'translateText', 'text': text, 'to_language_code': to_language_code, 'tone': tone})

    async def translate_message_text(self, chat_id: int = None, message_id: int = None, to_language_code: str = None, tone: str = None) -> FormattedText:
        """
        description Extracts text or caption of the given message and translates it to the given language; must not be used in secret chats. If the current user is a Telegram Premium user, then text formatting is preserved
        chat_id Identifier of the chat to which the message belongs
        message_id Identifier of the message
        to_language_code Language code of the language to which the message is translated. See translateText.to_language_code for the list of supported values
        tone Tone of the translation; see translateText.tone for the list of supported values
        """
        return await self._client.call_method('translateMessageText', {'@type': 'translateMessageText', 'chat_id': chat_id, 'message_id': message_id, 'to_language_code': to_language_code, 'tone': tone})

    async def summarize_message(self, chat_id: int = None, message_id: int = None, translate_to_language_code: str = None, tone: str = None) -> FormattedText:
        """
        description Summarizes content of the message with non-empty summary_language_code
        chat_id Identifier of the chat to which the message belongs
        message_id Identifier of the message
        translate_to_language_code Pass a language code to which the summary will be translated; pass an empty string if translation isn't needed. See translateText.to_language_code for the list of supported values
        tone Tone of the summarization; see translateText.tone for the list of supported values
        """
        return await self._client.call_method('summarizeMessage', {'@type': 'summarizeMessage', 'chat_id': chat_id, 'message_id': message_id, 'translate_to_language_code': translate_to_language_code, 'tone': tone})

    async def compose_text_with_ai(self, text: formattedText = None, translate_to_language_code: str = None, style_name: str = None, add_emojis: bool = None) -> FormattedText:
        """
        description Changes text using an AI model; must not be used in secret chats. May return an error with a message "AICOMPOSE_FLOOD_PREMIUM" if Telegram Premium is required to send further requests
        text The original text
        translate_to_language_code Pass a language code to which the text will be translated; pass an empty string if translation isn't needed. See translateText.to_language_code for the list of supported values
        style_name Name of the style of the resulted text; handle updateTextCompositionStyles to get the list of supported styles; pass an empty string to keep the current style of the text
        add_emojis Pass true to add emoji to the text
        """
        return await self._client.call_method('composeTextWithAi', {'@type': 'composeTextWithAi', 'text': text, 'translate_to_language_code': translate_to_language_code, 'style_name': style_name, 'add_emojis': add_emojis})

    async def fix_text_with_ai(self, text: formattedText = None) -> FixedText:
        """
        description Fixes text using an AI model; must not be used in secret chats. May return an error with a message "AICOMPOSE_FLOOD_PREMIUM" if Telegram Premium is required to send further requests
        text The original text
        """
        return await self._client.call_method('fixTextWithAi', {'@type': 'fixTextWithAi', 'text': text})

    async def recognize_speech(self, chat_id: int = None, message_id: int = None) -> Ok:
        """
        description Recognizes speech in a video note or a voice note message
        chat_id Identifier of the chat to which the message belongs
        message_id Identifier of the message. Use messageProperties.can_recognize_speech to check whether the message is suitable
        """
        return await self._client.call_method('recognizeSpeech', {'@type': 'recognizeSpeech', 'chat_id': chat_id, 'message_id': message_id})

    async def rate_speech_recognition(self, chat_id: int = None, message_id: int = None, is_good: bool = None) -> Ok:
        """
        description Rates recognized speech in a video note or a voice note message @chat_id Identifier of the chat to which the message belongs @message_id Identifier of the message @is_good Pass true if the speech recognition is good
        """
        return await self._client.call_method('rateSpeechRecognition', {'@type': 'rateSpeechRecognition', 'chat_id': chat_id, 'message_id': message_id, 'is_good': is_good})

    async def get_chat_available_message_senders(self, chat_id: int = None) -> ChatMessageSenders:
        """
        description Returns the list of message sender identifiers, which can be used to send messages in a chat @chat_id Chat identifier
        """
        return await self._client.call_method('getChatAvailableMessageSenders', {'@type': 'getChatAvailableMessageSenders', 'chat_id': chat_id})

    async def set_chat_message_sender(self, chat_id: int = None, message_sender_id: MessageSender = None) -> Ok:
        """
        description Selects a message sender to send messages in a chat @chat_id Chat identifier @message_sender_id New message sender for the chat
        """
        return await self._client.call_method('setChatMessageSender', {'@type': 'setChatMessageSender', 'chat_id': chat_id, 'message_sender_id': message_sender_id})

    async def send_message(self, chat_id: int = None, topic_id: MessageTopic = None, reply_to: InputMessageReplyTo = None, options: messageSendOptions = None, reply_markup: ReplyMarkup = None, input_message_content: InputMessageContent = None) -> Message:
        """
        description Sends a message. Returns the sent message
        chat_id Target chat
        topic_id Topic in which the message will be sent; pass null if none
        reply_to Information about the message or story to be replied; pass null if none
        options Options to be used to send the message; pass null to use default options
        reply_markup Markup for replying to the message; pass null if none; for bots only
        input_message_content The content of the message to be sent
        """
        return await self._client.call_method('sendMessage', {'@type': 'sendMessage', 'chat_id': chat_id, 'topic_id': topic_id, 'reply_to': reply_to, 'options': options, 'reply_markup': reply_markup, 'input_message_content': input_message_content})

    async def send_message_album(self, chat_id: int = None, topic_id: MessageTopic = None, reply_to: InputMessageReplyTo = None, options: messageSendOptions = None, input_message_contents: List[InputMessageContent] = None) -> Messages:
        """
        description Sends 2-10 messages grouped together into an album. Currently, only audio, document, photo and video messages can be grouped into an album.
        chat_id Target chat
        topic_id Topic in which the messages will be sent; pass null if none
        reply_to Information about the message or story to be replied; pass null if none
        options Options to be used to send the messages; pass null to use default options
        input_message_contents Contents of messages to be sent. At most 10 messages can be added to an album. All messages must have the same value of show_caption_above_media
        """
        return await self._client.call_method('sendMessageAlbum', {'@type': 'sendMessageAlbum', 'chat_id': chat_id, 'topic_id': topic_id, 'reply_to': reply_to, 'options': options, 'input_message_contents': input_message_contents})

    async def send_bot_start_message(self, bot_user_id: int = None, chat_id: int = None, parameter: str = None) -> Message:
        """
        description Invites a bot to a chat (if it is not yet a member) and sends it the /start command; requires can_invite_users member right. Bots can't be invited to a private chat other than the chat with the bot.
        bot_user_id Identifier of the bot
        chat_id Identifier of the target chat
        parameter A hidden parameter sent to the bot for deep linking purposes (https://core.telegram.org/bots#deep-linking)
        """
        return await self._client.call_method('sendBotStartMessage', {'@type': 'sendBotStartMessage', 'bot_user_id': bot_user_id, 'chat_id': chat_id, 'parameter': parameter})

    async def send_inline_query_result_message(self, chat_id: int = None, topic_id: MessageTopic = None, reply_to: InputMessageReplyTo = None, options: messageSendOptions = None, query_id: int = None, result_id: str = None, hide_via_bot: bool = None) -> Message:
        """
        description Sends the result of an inline query as a message. Returns the sent message. Always clears a chat draft message
        chat_id Target chat
        topic_id Topic in which the message will be sent; pass null if none
        reply_to Information about the message or story to be replied; pass null if none
        options Options to be used to send the message; pass null to use default options
        query_id Identifier of the inline query
        result_id Identifier of the inline query result
        hide_via_bot Pass true to hide the bot, via which the message is sent. Can be used only for bots getOption("animation_search_bot_username"), getOption("photo_search_bot_username"), and getOption("venue_search_bot_username")
        """
        return await self._client.call_method('sendInlineQueryResultMessage', {'@type': 'sendInlineQueryResultMessage', 'chat_id': chat_id, 'topic_id': topic_id, 'reply_to': reply_to, 'options': options, 'query_id': query_id, 'result_id': result_id, 'hide_via_bot': hide_via_bot})

    async def forward_messages(self, chat_id: int = None, topic_id: MessageTopic = None, from_chat_id: int = None, message_ids: List[int] = None, options: messageSendOptions = None, send_copy: bool = None, remove_caption: bool = None) -> Messages:
        """
        description Forwards previously sent messages. Returns the forwarded messages in the same order as the message identifiers passed in message_ids. If a message can't be forwarded, null will be returned instead of the message
        chat_id Identifier of the chat to which to forward messages
        topic_id Topic in which the messages will be forwarded; message threads aren't supported; pass null if none
        from_chat_id Identifier of the chat from which to forward messages
        message_ids Identifiers of the messages to forward. Message identifiers must be in a strictly increasing order. At most 100 messages can be forwarded simultaneously. A message can be forwarded only if messageProperties.can_be_forwarded
        options Options to be used to send the messages; pass null to use default options
        send_copy Pass true to copy content of the messages without reference to the original sender. Always true if the messages are forwarded to a secret chat or are local.
        remove_caption Pass true to remove media captions of message copies. Ignored if send_copy is false
        """
        return await self._client.call_method('forwardMessages', {'@type': 'forwardMessages', 'chat_id': chat_id, 'topic_id': topic_id, 'from_chat_id': from_chat_id, 'message_ids': message_ids, 'options': options, 'send_copy': send_copy, 'remove_caption': remove_caption})

    async def forward_messages_with_confirmation(self, chat_id: int = None, topic_id: MessageTopic = None, from_chat_id: int = None, message_ids: List[int] = None, options: messageSendOptions = None, send_copy: bool = None, remove_caption: bool = None, confirmation_timeout: float = 5.0) -> Messages:
        """Forward messages and wait for final message IDs.

        Like forward_messages, but waits for updateMessageSendSucceeded so
        the returned message objects contain the final (not temporary) IDs.
        """
        result = await self.forward_messages(
            chat_id=chat_id,
            topic_id=topic_id,
            from_chat_id=from_chat_id,
            message_ids=message_ids,
            options=options,
            send_copy=send_copy,
            remove_caption=remove_caption,
        )

        if not result or not getattr(result, 'messages', None):
            return result

        msgs = result.messages
        if not msgs:
            return result

        from grathon.high_level.helpers.message_tracker import get_message_tracker
        tracker = get_message_tracker()
        updated = False

        for i, msg in enumerate(msgs):
            if msg is None or not hasattr(msg, 'id'):
                continue
            pending_id = msg.id
            try:
                future = await tracker.track_pending(
                    chat_id=chat_id,
                    pending_message_id=pending_id,
                    timeout=confirmation_timeout,
                )
                final_id = await asyncio.wait_for(future, timeout=confirmation_timeout + 1)
                if isinstance(final_id, int):
                    msgs[i].id = final_id
                    updated = True
            except asyncio.TimeoutError:
                print(f"[FORWARD CONFIRM] TIMEOUT waiting for final_id for pending_id={pending_id}")
            except Exception as e:
                print(f"[FORWARD CONFIRM] ERROR: {e}")

        return result

    async def send_quick_reply_shortcut_messages(self, chat_id: int = None, shortcut_id: int = None, sending_id: int = None) -> Messages:
        """
        description Sends messages from a quick reply shortcut. Requires Telegram Business subscription. Can't be used to send paid messages
        chat_id Identifier of the chat to which to send messages. The chat must be a private chat with a regular user
        shortcut_id Unique identifier of the quick reply shortcut
        sending_id Non-persistent identifier, which will be returned back in messageSendingStatePending object and can be used to match sent messages and corresponding updateNewMessage updates
        """
        return await self._client.call_method('sendQuickReplyShortcutMessages', {'@type': 'sendQuickReplyShortcutMessages', 'chat_id': chat_id, 'shortcut_id': shortcut_id, 'sending_id': sending_id})

    async def resend_messages(self, chat_id: int = None, message_ids: List[int] = None, quote: inputTextQuote = None, paid_message_star_count: int = None) -> Messages:
        """
        description Resends messages which failed to send. Can be called only for messages for which messageSendingStateFailed.can_retry is true and after specified in messageSendingStateFailed.retry_after time passed.
        chat_id Identifier of the chat to send messages
        message_ids Identifiers of the messages to resend. Message identifiers must be in a strictly increasing order
        quote New manually chosen quote from the message to be replied; pass null if none. Ignored if more than one message is re-sent, or if messageSendingStateFailed.need_another_reply_quote == false
        paid_message_star_count The number of Telegram Stars the user agreed to pay to send the messages. Ignored if messageSendingStateFailed.required_paid_message_star_count == 0
        """
        return await self._client.call_method('resendMessages', {'@type': 'resendMessages', 'chat_id': chat_id, 'message_ids': message_ids, 'quote': quote, 'paid_message_star_count': paid_message_star_count})

    async def add_local_message(self, chat_id: int = None, sender_id: MessageSender = None, reply_to: InputMessageReplyTo = None, disable_notification: bool = None, input_message_content: InputMessageContent = None) -> Message:
        """
        description Adds a local message to a chat. The message is persistent across application restarts only if the message database is used. Returns the added message
        chat_id Target chat; channel direct messages chats aren't supported
        sender_id Identifier of the sender of the message
        reply_to Information about the message or story to be replied; pass null if none
        disable_notification Pass true to disable notification for the message
        input_message_content The content of the message to be added
        """
        return await self._client.call_method('addLocalMessage', {'@type': 'addLocalMessage', 'chat_id': chat_id, 'sender_id': sender_id, 'reply_to': reply_to, 'disable_notification': disable_notification, 'input_message_content': input_message_content})

    async def delete_messages(self, chat_id: int = None, message_ids: List[int] = None, revoke: bool = None) -> Ok:
        """
        description Deletes messages
        chat_id Chat identifier
        message_ids Identifiers of the messages to be deleted. Use messageProperties.can_be_deleted_only_for_self and messageProperties.can_be_deleted_for_all_users to get suitable messages
        revoke Pass true to delete messages for all chat members. Always true for supergroups, channels and secret chats
        """
        return await self._client.call_method('deleteMessages', {'@type': 'deleteMessages', 'chat_id': chat_id, 'message_ids': message_ids, 'revoke': revoke})

    async def delete_chat_messages_by_sender(self, chat_id: int = None, sender_id: MessageSender = None) -> Ok:
        """
        description Deletes all messages sent by the specified message sender in a chat. Supported only for supergroups; requires can_delete_messages administrator right @chat_id Chat identifier @sender_id Identifier of the sender of messages to delete
        """
        return await self._client.call_method('deleteChatMessagesBySender', {'@type': 'deleteChatMessagesBySender', 'chat_id': chat_id, 'sender_id': sender_id})

    async def delete_chat_messages_by_date(self, chat_id: int = None, min_date: int = None, max_date: int = None, revoke: bool = None) -> Ok:
        """
        description Deletes all messages between the specified dates in a chat. Supported only for private chats and basic groups. Messages sent in the last 30 seconds will not be deleted
        chat_id Chat identifier
        min_date The minimum date of the messages to delete
        max_date The maximum date of the messages to delete
        revoke Pass true to delete chat messages for all users; private chats only
        """
        return await self._client.call_method('deleteChatMessagesByDate', {'@type': 'deleteChatMessagesByDate', 'chat_id': chat_id, 'min_date': min_date, 'max_date': max_date, 'revoke': revoke})

    async def edit_message_text(self, chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, input_message_content: InputMessageContent = None) -> Message:
        """
        description Edits the text of a message (or a text of a game message). Returns the edited message after the edit is completed on the server side
        chat_id The chat the message belongs to
        message_id Identifier of the message. Use messageProperties.can_be_edited to check whether the message can be edited
        reply_markup The new message reply markup; pass null if none; for bots only
        input_message_content New text content of the message. Must be of type inputMessageText or inputMessageRichMessage
        """
        return await self._client.call_method('editMessageText', {'@type': 'editMessageText', 'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply_markup, 'input_message_content': input_message_content})

    async def edit_message_live_location(self, chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, location: liveLocation = None) -> Message:
        """
        description Edits the message content of a live location. Messages can be edited for a limited period of time specified in the live location.
        chat_id The chat the message belongs to
        message_id Identifier of the message. Use messageProperties.can_be_edited to check whether the message can be edited
        reply_markup The new message reply markup; pass null if none; for bots only
        location New live location of the message; pass null to stop sharing the live location. If the new live_period isn't set to 0x7FFFFFFF,
        """
        return await self._client.call_method('editMessageLiveLocation', {'@type': 'editMessageLiveLocation', 'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply_markup, 'location': location})

    async def edit_message_checklist(self, chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, checklist: inputChecklist = None) -> Message:
        """
        description Edits the message content of a checklist. Returns the edited message after the edit is completed on the server side
        chat_id The chat the message belongs to
        message_id Identifier of the message. Use messageProperties.can_be_edited to check whether the message can be edited
        reply_markup The new message reply markup; pass null if none; for bots only
        checklist The new checklist. If some tasks were completed, this information will be kept
        """
        return await self._client.call_method('editMessageChecklist', {'@type': 'editMessageChecklist', 'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply_markup, 'checklist': checklist})

    async def edit_message_media(self, chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, input_message_content: InputMessageContent = None) -> Message:
        """
        description Edits the media content of a message, including message caption. If only the caption needs to be edited, use editMessageCaption instead.
        chat_id The chat the message belongs to
        message_id Identifier of the message. Use messageProperties.can_edit_media to check whether the message can be edited
        reply_markup The new message reply markup; pass null if none; for bots only
        input_message_content New content of the message. Must be one of the following types: inputMessageAnimation, inputMessageAudio, inputMessageDocument, inputMessagePhoto or inputMessageVideo
        """
        return await self._client.call_method('editMessageMedia', {'@type': 'editMessageMedia', 'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply_markup, 'input_message_content': input_message_content})

    async def edit_message_caption(self, chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, caption: formattedText = None, show_caption_above_media: bool = None) -> Message:
        """
        description Edits the message content caption. Returns the edited message after the edit is completed on the server side
        chat_id The chat the message belongs to
        message_id Identifier of the message. Use messageProperties.can_be_edited to check whether the message can be edited
        reply_markup The new message reply markup; pass null if none; for bots only
        caption New message content caption; 0-getOption("message_caption_length_max") characters; pass null to remove caption
        show_caption_above_media Pass true to show the caption above the media; otherwise, the caption will be shown below the media. May be true only for animation, photo, and video messages
        """
        return await self._client.call_method('editMessageCaption', {'@type': 'editMessageCaption', 'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply_markup, 'caption': caption, 'show_caption_above_media': show_caption_above_media})

    async def edit_message_reply_markup(self, chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None) -> Message:
        """
        description Edits the message reply markup; for bots only. Returns the edited message after the edit is completed on the server side
        chat_id The chat the message belongs to
        message_id Identifier of the message. Use messageProperties.can_be_edited to check whether the message can be edited
        reply_markup The new message reply markup; pass null if none
        """
        return await self._client.call_method('editMessageReplyMarkup', {'@type': 'editMessageReplyMarkup', 'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply_markup})

    async def edit_inline_message_text(self, inline_message_id: str = None, reply_markup: ReplyMarkup = None, input_message_content: InputMessageContent = None) -> Ok:
        """
        description Edits the text of an inline text or game message sent via a bot; for bots only
        inline_message_id Inline message identifier
        reply_markup The new message reply markup; pass null if none
        input_message_content New text content of the message. Must be of type inputMessageText or inputMessageRichMessage
        """
        return await self._client.call_method('editInlineMessageText', {'@type': 'editInlineMessageText', 'inline_message_id': inline_message_id, 'reply_markup': reply_markup, 'input_message_content': input_message_content})

    async def edit_inline_message_live_location(self, inline_message_id: str = None, reply_markup: ReplyMarkup = None, location: liveLocation = None) -> Ok:
        """
        description Edits the content of a live location in an inline message sent via a bot; for bots only
        inline_message_id Inline message identifier
        reply_markup The new message reply markup; pass null if none
        location New live location of the message; pass null to stop sharing the live location. If the new live_period isn't set to 0x7FFFFFFF,
        """
        return await self._client.call_method('editInlineMessageLiveLocation', {'@type': 'editInlineMessageLiveLocation', 'inline_message_id': inline_message_id, 'reply_markup': reply_markup, 'location': location})

    async def edit_inline_message_media(self, inline_message_id: str = None, reply_markup: ReplyMarkup = None, input_message_content: InputMessageContent = None) -> Ok:
        """
        description Edits the media content of a message with a text, an animation, an audio, a document, a photo or a video in an inline message sent via a bot; for bots only
        inline_message_id Inline message identifier
        reply_markup The new message reply markup; pass null if none; for bots only
        input_message_content New content of the message. Must be one of the following types: inputMessageAnimation, inputMessageAudio, inputMessageDocument, inputMessagePhoto or inputMessageVideo
        """
        return await self._client.call_method('editInlineMessageMedia', {'@type': 'editInlineMessageMedia', 'inline_message_id': inline_message_id, 'reply_markup': reply_markup, 'input_message_content': input_message_content})

    async def edit_inline_message_caption(self, inline_message_id: str = None, reply_markup: ReplyMarkup = None, caption: formattedText = None, show_caption_above_media: bool = None) -> Ok:
        """
        description Edits the caption of an inline message sent via a bot; for bots only
        inline_message_id Inline message identifier
        reply_markup The new message reply markup; pass null if none
        caption New message content caption; pass null to remove caption; 0-getOption("message_caption_length_max") characters
        show_caption_above_media Pass true to show the caption above the media; otherwise, the caption will be shown below the media. May be true only for animation, photo, and video messages
        """
        return await self._client.call_method('editInlineMessageCaption', {'@type': 'editInlineMessageCaption', 'inline_message_id': inline_message_id, 'reply_markup': reply_markup, 'caption': caption, 'show_caption_above_media': show_caption_above_media})

    async def edit_inline_message_reply_markup(self, inline_message_id: str = None, reply_markup: ReplyMarkup = None) -> Ok:
        """
        description Edits the reply markup of an inline message sent via a bot; for bots only
        inline_message_id Inline message identifier
        reply_markup The new message reply markup; pass null if none
        """
        return await self._client.call_method('editInlineMessageReplyMarkup', {'@type': 'editInlineMessageReplyMarkup', 'inline_message_id': inline_message_id, 'reply_markup': reply_markup})

    async def edit_message_scheduling_state(self, chat_id: int = None, message_id: int = None, scheduling_state: MessageSchedulingState = None) -> Ok:
        """
        description Edits the time when a scheduled message will be sent. Scheduling state of all messages in the same album or forwarded together with the message will be also changed
        chat_id The chat the message belongs to
        message_id Identifier of the message. Use messageProperties.can_edit_scheduling_state to check whether the message is suitable
        scheduling_state The new message scheduling state; pass null to send the message immediately. Must be null for messages in the state messageSchedulingStateSendWhenVideoProcessed
        """
        return await self._client.call_method('editMessageSchedulingState', {'@type': 'editMessageSchedulingState', 'chat_id': chat_id, 'message_id': message_id, 'scheduling_state': scheduling_state})

    async def set_message_fact_check(self, chat_id: int = None, message_id: int = None, text: formattedText = None) -> Ok:
        """
        description Changes the fact-check of a message. Can be only used if messageProperties.can_set_fact_check == true
        chat_id The channel chat the message belongs to
        message_id Identifier of the message
        text New text of the fact-check; 0-getOption("fact_check_length_max") characters; pass null to remove it. Only Bold, Italic, and TextUrl entities with https://t.me/ links are supported
        """
        return await self._client.call_method('setMessageFactCheck', {'@type': 'setMessageFactCheck', 'chat_id': chat_id, 'message_id': message_id, 'text': text})

    async def send_business_message(self, business_connection_id: str = None, chat_id: int = None, reply_to: InputMessageReplyTo = None, disable_notification: bool = None, protect_content: bool = None, effect_id: int = None, reply_markup: ReplyMarkup = None, input_message_content: InputMessageContent = None) -> BusinessMessage:
        """
        description Sends a message on behalf of a business account; for bots only. Returns the message after it was sent
        business_connection_id Unique identifier of business connection on behalf of which to send the request
        chat_id Target chat
        reply_to Information about the message to be replied; pass null if none
        disable_notification Pass true to disable notification for the message
        protect_content Pass true if the content of the message must be protected from forwarding and saving
        effect_id Identifier of the effect to apply to the message
        reply_markup Markup for replying to the message; pass null if none
        input_message_content The content of the message to be sent
        """
        return await self._client.call_method('sendBusinessMessage', {'@type': 'sendBusinessMessage', 'business_connection_id': business_connection_id, 'chat_id': chat_id, 'reply_to': reply_to, 'disable_notification': disable_notification, 'protect_content': protect_content, 'effect_id': effect_id, 'reply_markup': reply_markup, 'input_message_content': input_message_content})

    async def send_business_message_album(self, business_connection_id: str = None, chat_id: int = None, reply_to: InputMessageReplyTo = None, disable_notification: bool = None, protect_content: bool = None, effect_id: int = None, input_message_contents: List[InputMessageContent] = None) -> BusinessMessages:
        """
        description Sends 2-10 messages grouped together into an album on behalf of a business account; for bots only. Currently, only audio, document, photo and video messages can be grouped into an album.
        business_connection_id Unique identifier of business connection on behalf of which to send the request
        chat_id Target chat
        reply_to Information about the message to be replied; pass null if none
        disable_notification Pass true to disable notification for the message
        protect_content Pass true if the content of the message must be protected from forwarding and saving
        effect_id Identifier of the effect to apply to the message
        input_message_contents Contents of messages to be sent. At most 10 messages can be added to an album. All messages must have the same value of show_caption_above_media
        """
        return await self._client.call_method('sendBusinessMessageAlbum', {'@type': 'sendBusinessMessageAlbum', 'business_connection_id': business_connection_id, 'chat_id': chat_id, 'reply_to': reply_to, 'disable_notification': disable_notification, 'protect_content': protect_content, 'effect_id': effect_id, 'input_message_contents': input_message_contents})

    async def edit_business_message_text(self, business_connection_id: str = None, chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, input_message_content: InputMessageContent = None) -> BusinessMessage:
        """
        description Edits the text of a text or game message sent on behalf of a business account; for bots only
        business_connection_id Unique identifier of business connection on behalf of which the message was sent
        chat_id The chat the message belongs to
        message_id Identifier of the message
        reply_markup The new message reply markup; pass null if none
        input_message_content New text content of the message. Must be of type inputMessageText or inputMessageRichMessage
        """
        return await self._client.call_method('editBusinessMessageText', {'@type': 'editBusinessMessageText', 'business_connection_id': business_connection_id, 'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply_markup, 'input_message_content': input_message_content})

    async def edit_business_message_live_location(self, business_connection_id: str = None, chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, location: liveLocation = None) -> BusinessMessage:
        """
        description Edits the content of a live location in a message sent on behalf of a business account; for bots only
        business_connection_id Unique identifier of business connection on behalf of which the message was sent
        chat_id The chat the message belongs to
        message_id Identifier of the message
        reply_markup The new message reply markup; pass null if none
        location New live location of the message; pass null to stop sharing the live location. If the new live_period isn't set to 0x7FFFFFFF,
        """
        return await self._client.call_method('editBusinessMessageLiveLocation', {'@type': 'editBusinessMessageLiveLocation', 'business_connection_id': business_connection_id, 'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply_markup, 'location': location})

    async def edit_business_message_checklist(self, business_connection_id: str = None, chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, checklist: inputChecklist = None) -> BusinessMessage:
        """
        description Edits the content of a checklist in a message sent on behalf of a business account; for bots only
        business_connection_id Unique identifier of business connection on behalf of which the message was sent
        chat_id The chat the message belongs to
        message_id Identifier of the message
        reply_markup The new message reply markup; pass null if none
        checklist The new checklist. If some tasks were completed, this information will be kept
        """
        return await self._client.call_method('editBusinessMessageChecklist', {'@type': 'editBusinessMessageChecklist', 'business_connection_id': business_connection_id, 'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply_markup, 'checklist': checklist})

    async def edit_business_message_media(self, business_connection_id: str = None, chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, input_message_content: InputMessageContent = None) -> BusinessMessage:
        """
        description Edits the media content of a message with a text, an animation, an audio, a document, a photo or a video in a message sent on behalf of a business account; for bots only
        business_connection_id Unique identifier of business connection on behalf of which the message was sent
        chat_id The chat the message belongs to
        message_id Identifier of the message
        reply_markup The new message reply markup; pass null if none; for bots only
        input_message_content New content of the message. Must be one of the following types: inputMessageAnimation, inputMessageAudio, inputMessageDocument, inputMessagePhoto or inputMessageVideo
        """
        return await self._client.call_method('editBusinessMessageMedia', {'@type': 'editBusinessMessageMedia', 'business_connection_id': business_connection_id, 'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply_markup, 'input_message_content': input_message_content})

    async def edit_business_message_caption(self, business_connection_id: str = None, chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None, caption: formattedText = None, show_caption_above_media: bool = None) -> BusinessMessage:
        """
        description Edits the caption of a message sent on behalf of a business account; for bots only
        business_connection_id Unique identifier of business connection on behalf of which the message was sent
        chat_id The chat the message belongs to
        message_id Identifier of the message
        reply_markup The new message reply markup; pass null if none
        caption New message content caption; pass null to remove caption; 0-getOption("message_caption_length_max") characters
        show_caption_above_media Pass true to show the caption above the media; otherwise, the caption will be shown below the media. May be true only for animation, photo, and video messages
        """
        return await self._client.call_method('editBusinessMessageCaption', {'@type': 'editBusinessMessageCaption', 'business_connection_id': business_connection_id, 'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply_markup, 'caption': caption, 'show_caption_above_media': show_caption_above_media})

    async def edit_business_message_reply_markup(self, business_connection_id: str = None, chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None) -> BusinessMessage:
        """
        description Edits the reply markup of a message sent on behalf of a business account; for bots only
        business_connection_id Unique identifier of business connection on behalf of which the message was sent
        chat_id The chat the message belongs to
        message_id Identifier of the message
        reply_markup The new message reply markup; pass null if none
        """
        return await self._client.call_method('editBusinessMessageReplyMarkup', {'@type': 'editBusinessMessageReplyMarkup', 'business_connection_id': business_connection_id, 'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply_markup})

    async def stop_business_poll(self, business_connection_id: str = None, chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None) -> BusinessMessage:
        """
        description Stops a poll sent on behalf of a business account; for bots only
        business_connection_id Unique identifier of business connection on behalf of which the message with the poll was sent
        chat_id The chat the message belongs to
        message_id Identifier of the message containing the poll
        reply_markup The new message reply markup; pass null if none
        """
        return await self._client.call_method('stopBusinessPoll', {'@type': 'stopBusinessPoll', 'business_connection_id': business_connection_id, 'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply_markup})

    async def set_business_message_is_pinned(self, business_connection_id: str = None, chat_id: int = None, message_id: int = None, is_pinned: bool = None) -> Ok:
        """
        description Pins or unpins a message sent on behalf of a business account; for bots only
        business_connection_id Unique identifier of business connection on behalf of which the message was sent
        chat_id The chat the message belongs to
        message_id Identifier of the message
        is_pinned Pass true to pin the message, pass false to unpin it
        """
        return await self._client.call_method('setBusinessMessageIsPinned', {'@type': 'setBusinessMessageIsPinned', 'business_connection_id': business_connection_id, 'chat_id': chat_id, 'message_id': message_id, 'is_pinned': is_pinned})

    async def read_business_message(self, business_connection_id: str = None, chat_id: int = None, message_id: int = None) -> Ok:
        """
        description Reads a message on behalf of a business account; for bots only
        business_connection_id Unique identifier of business connection through which the message was received
        chat_id The chat the message belongs to
        message_id Identifier of the message
        """
        return await self._client.call_method('readBusinessMessage', {'@type': 'readBusinessMessage', 'business_connection_id': business_connection_id, 'chat_id': chat_id, 'message_id': message_id})

    async def delete_business_messages(self, business_connection_id: str = None, message_ids: List[int] = None) -> Ok:
        """
        description Deletes messages on behalf of a business account; for bots only
        business_connection_id Unique identifier of business connection through which the messages were received
        message_ids Identifier of the messages
        """
        return await self._client.call_method('deleteBusinessMessages', {'@type': 'deleteBusinessMessages', 'business_connection_id': business_connection_id, 'message_ids': message_ids})

    async def edit_business_story(self, story_poster_chat_id: int = None, story_id: int = None, content: InputStoryContent = None, areas: inputStoryAreas = None, caption: formattedText = None, privacy_settings: StoryPrivacySettings = None) -> Story:
        """
        description Changes a story posted by the bot on behalf of a business account; for bots only
        story_poster_chat_id Identifier of the chat that posted the story
        story_id Identifier of the story to edit
        content New content of the story
        areas New clickable rectangle areas to be shown on the story media
        caption New story caption
        privacy_settings The new privacy settings for the story
        """
        return await self._client.call_method('editBusinessStory', {'@type': 'editBusinessStory', 'story_poster_chat_id': story_poster_chat_id, 'story_id': story_id, 'content': content, 'areas': areas, 'caption': caption, 'privacy_settings': privacy_settings})

    async def delete_business_story(self, business_connection_id: str = None, story_id: int = None) -> Ok:
        """
        description Deletes a story posted by the bot on behalf of a business account; for bots only
        business_connection_id Unique identifier of business connection
        story_id Identifier of the story to delete
        """
        return await self._client.call_method('deleteBusinessStory', {'@type': 'deleteBusinessStory', 'business_connection_id': business_connection_id, 'story_id': story_id})

    async def set_business_account_name(self, business_connection_id: str = None, first_name: str = None, last_name: str = None) -> Ok:
        """
        description Changes the first and last name of a business account; for bots only
        business_connection_id Unique identifier of business connection
        first_name The new value of the first name for the business account; 1-64 characters
        last_name The new value of the optional last name for the business account; 0-64 characters
        """
        return await self._client.call_method('setBusinessAccountName', {'@type': 'setBusinessAccountName', 'business_connection_id': business_connection_id, 'first_name': first_name, 'last_name': last_name})

    async def set_business_account_bio(self, business_connection_id: str = None, bio: str = None) -> Ok:
        """
        description Changes the bio of a business account; for bots only
        business_connection_id Unique identifier of business connection
        bio The new value of the bio; 0-getOption("bio_length_max") characters without line feeds
        """
        return await self._client.call_method('setBusinessAccountBio', {'@type': 'setBusinessAccountBio', 'business_connection_id': business_connection_id, 'bio': bio})

    async def set_business_account_profile_photo(self, business_connection_id: str = None, photo: InputChatPhoto = None, is_public: bool = None) -> Ok:
        """
        description Changes a profile photo of a business account; for bots only
        business_connection_id Unique identifier of business connection
        photo Profile photo to set; pass null to remove the photo
        is_public Pass true to set the public photo, which will be visible even if the main photo is hidden by privacy settings
        """
        return await self._client.call_method('setBusinessAccountProfilePhoto', {'@type': 'setBusinessAccountProfilePhoto', 'business_connection_id': business_connection_id, 'photo': photo, 'is_public': is_public})

    async def set_business_account_username(self, business_connection_id: str = None, username: str = None) -> Ok:
        """
        description Changes the editable username of a business account; for bots only
        business_connection_id Unique identifier of business connection
        username The new value of the username
        """
        return await self._client.call_method('setBusinessAccountUsername', {'@type': 'setBusinessAccountUsername', 'business_connection_id': business_connection_id, 'username': username})

    async def set_business_account_gift_settings(self, business_connection_id: str = None, settings: giftSettings = None) -> Ok:
        """
        description Changes settings for gift receiving of a business account; for bots only
        business_connection_id Unique identifier of business connection
        settings The new settings
        """
        return await self._client.call_method('setBusinessAccountGiftSettings', {'@type': 'setBusinessAccountGiftSettings', 'business_connection_id': business_connection_id, 'settings': settings})

    async def get_business_account_star_amount(self, business_connection_id: str = None) -> StarAmount:
        """
        description Returns the Telegram Star amount owned by a business account; for bots only @business_connection_id Unique identifier of business connection
        """
        return await self._client.call_method('getBusinessAccountStarAmount', {'@type': 'getBusinessAccountStarAmount', 'business_connection_id': business_connection_id})

    async def transfer_business_account_stars(self, business_connection_id: str = None, star_count: int = None) -> Ok:
        """
        description Transfers Telegram Stars from the business account to the business bot; for bots only
        business_connection_id Unique identifier of business connection
        star_count Number of Telegram Stars to transfer
        """
        return await self._client.call_method('transferBusinessAccountStars', {'@type': 'transferBusinessAccountStars', 'business_connection_id': business_connection_id, 'star_count': star_count})

    async def check_quick_reply_shortcut_name(self, name: str = None) -> Ok:
        """
        description Checks validness of a name for a quick reply shortcut. Can be called synchronously @name The name of the shortcut; 1-32 characters
        """
        return await self._client.call_method('checkQuickReplyShortcutName', {'@type': 'checkQuickReplyShortcutName', 'name': name})

    async def load_quick_reply_shortcuts(self) -> Ok:
        """
        description Loads quick reply shortcuts created by the current user. The loaded data will be sent through updateQuickReplyShortcut and updateQuickReplyShortcuts
        """
        return await self._client.call_method('loadQuickReplyShortcuts', {'@type': 'loadQuickReplyShortcuts'})

    async def set_quick_reply_shortcut_name(self, shortcut_id: int = None, name: str = None) -> Ok:
        """
        description Changes name of a quick reply shortcut @shortcut_id Unique identifier of the quick reply shortcut @name New name for the shortcut. Use checkQuickReplyShortcutName to check its validness
        """
        return await self._client.call_method('setQuickReplyShortcutName', {'@type': 'setQuickReplyShortcutName', 'shortcut_id': shortcut_id, 'name': name})

    async def delete_quick_reply_shortcut(self, shortcut_id: int = None) -> Ok:
        """
        description Deletes a quick reply shortcut @shortcut_id Unique identifier of the quick reply shortcut
        """
        return await self._client.call_method('deleteQuickReplyShortcut', {'@type': 'deleteQuickReplyShortcut', 'shortcut_id': shortcut_id})

    async def reorder_quick_reply_shortcuts(self, shortcut_ids: List[int] = None) -> Ok:
        """
        description Changes the order of quick reply shortcuts @shortcut_ids The new order of quick reply shortcuts
        """
        return await self._client.call_method('reorderQuickReplyShortcuts', {'@type': 'reorderQuickReplyShortcuts', 'shortcut_ids': shortcut_ids})

    async def load_quick_reply_shortcut_messages(self, shortcut_id: int = None) -> Ok:
        """
        description Loads quick reply messages that can be sent by a given quick reply shortcut. The loaded messages will be sent through updateQuickReplyShortcutMessages
        shortcut_id Unique identifier of the quick reply shortcut
        """
        return await self._client.call_method('loadQuickReplyShortcutMessages', {'@type': 'loadQuickReplyShortcutMessages', 'shortcut_id': shortcut_id})

    async def delete_quick_reply_shortcut_messages(self, shortcut_id: int = None, message_ids: List[int] = None) -> Ok:
        """
        description Deletes specified quick reply messages
        shortcut_id Unique identifier of the quick reply shortcut to which the messages belong
        message_ids Unique identifiers of the messages
        """
        return await self._client.call_method('deleteQuickReplyShortcutMessages', {'@type': 'deleteQuickReplyShortcutMessages', 'shortcut_id': shortcut_id, 'message_ids': message_ids})

    async def add_quick_reply_shortcut_message(self, shortcut_name: str = None, reply_to_message_id: int = None, input_message_content: InputMessageContent = None) -> QuickReplyMessage:
        """
        description Adds a message to a quick reply shortcut. If shortcut doesn't exist and there are less than getOption("quick_reply_shortcut_count_max") shortcuts, then a new shortcut is created.
        shortcut_name Name of the target shortcut
        reply_to_message_id Identifier of a quick reply message in the same shortcut to be replied; pass 0 if none
        input_message_content The content of the message to be added; inputMessagePaidMedia, inputMessageForwarded and inputMessageLiveLocation
        """
        return await self._client.call_method('addQuickReplyShortcutMessage', {'@type': 'addQuickReplyShortcutMessage', 'shortcut_name': shortcut_name, 'reply_to_message_id': reply_to_message_id, 'input_message_content': input_message_content})

    async def add_quick_reply_shortcut_inline_query_result_message(self, shortcut_name: str = None, reply_to_message_id: int = None, query_id: int = None, result_id: str = None, hide_via_bot: bool = None) -> QuickReplyMessage:
        """
        description Adds a message to a quick reply shortcut via inline bot. If shortcut doesn't exist and there are less than getOption("quick_reply_shortcut_count_max") shortcuts, then a new shortcut is created.
        shortcut_name Name of the target shortcut
        reply_to_message_id Identifier of a quick reply message in the same shortcut to be replied; pass 0 if none
        query_id Identifier of the inline query
        result_id Identifier of the inline query result
        hide_via_bot Pass true to hide the bot, via which the message is sent. Can be used only for bots getOption("animation_search_bot_username"), getOption("photo_search_bot_username"), and getOption("venue_search_bot_username")
        """
        return await self._client.call_method('addQuickReplyShortcutInlineQueryResultMessage', {'@type': 'addQuickReplyShortcutInlineQueryResultMessage', 'shortcut_name': shortcut_name, 'reply_to_message_id': reply_to_message_id, 'query_id': query_id, 'result_id': result_id, 'hide_via_bot': hide_via_bot})

    async def add_quick_reply_shortcut_message_album(self, shortcut_name: str = None, reply_to_message_id: int = None, input_message_contents: List[InputMessageContent] = None) -> QuickReplyMessages:
        """
        description Adds 2-10 messages grouped together into an album to a quick reply shortcut. Currently, only audio, document, photo and video messages can be grouped into an album.
        shortcut_name Name of the target shortcut
        reply_to_message_id Identifier of a quick reply message in the same shortcut to be replied; pass 0 if none
        input_message_contents Contents of messages to be sent. At most 10 messages can be added to an album. All messages must have the same value of show_caption_above_media
        """
        return await self._client.call_method('addQuickReplyShortcutMessageAlbum', {'@type': 'addQuickReplyShortcutMessageAlbum', 'shortcut_name': shortcut_name, 'reply_to_message_id': reply_to_message_id, 'input_message_contents': input_message_contents})

    async def readd_quick_reply_shortcut_messages(self, shortcut_name: str = None, message_ids: List[int] = None) -> QuickReplyMessages:
        """
        description Readds quick reply messages which failed to add. Can be called only for messages for which messageSendingStateFailed.can_retry is true and after specified in messageSendingStateFailed.retry_after time passed.
        shortcut_name Name of the target shortcut
        message_ids Identifiers of the quick reply messages to readd. Message identifiers must be in a strictly increasing order
        """
        return await self._client.call_method('readdQuickReplyShortcutMessages', {'@type': 'readdQuickReplyShortcutMessages', 'shortcut_name': shortcut_name, 'message_ids': message_ids})

    async def edit_quick_reply_message(self, shortcut_id: int = None, message_id: int = None, input_message_content: InputMessageContent = None) -> Ok:
        """
        description Asynchronously edits the text, media or caption of a quick reply message. Use quickReplyMessage.can_be_edited to check whether a message can be edited.
        shortcut_id Unique identifier of the quick reply shortcut with the message
        message_id Identifier of the message
        input_message_content New content of the message. Must be one of the following types: inputMessageAnimation, inputMessageAudio, inputMessageChecklist, inputMessageDocument, inputMessagePhoto, inputMessageRichMessage, inputMessageText, or inputMessageVideo
        """
        return await self._client.call_method('editQuickReplyMessage', {'@type': 'editQuickReplyMessage', 'shortcut_id': shortcut_id, 'message_id': message_id, 'input_message_content': input_message_content})

    async def get_forum_topic_default_icons(self) -> Stickers:
        """
        description Returns the list of custom emoji, which can be used as forum topic icon by all users
        """
        return await self._client.call_method('getForumTopicDefaultIcons', {'@type': 'getForumTopicDefaultIcons'})

    async def create_forum_topic(self, chat_id: int = None, name: str = None, is_name_implicit: bool = None, icon: forumTopicIcon = None) -> ForumTopicInfo:
        """
        description Creates a topic in a forum supergroup chat or a chat with a bot with topics; requires can_manage_topics administrator or can_create_topics member right in the supergroup
        chat_id Identifier of the chat
        name Name of the topic; 1-128 characters
        is_name_implicit Pass true if the name of the topic wasn't entered explicitly; for chats with bots only
        icon Icon of the topic. Icon color must be one of 0x6FB9F0, 0xFFD67E, 0xCB86DB, 0x8EEE98, 0xFF93B2, or 0xFB6F5F. Telegram Premium users can use any custom emoji as topic icon, other users can use only a custom emoji returned by getForumTopicDefaultIcons
        """
        return await self._client.call_method('createForumTopic', {'@type': 'createForumTopic', 'chat_id': chat_id, 'name': name, 'is_name_implicit': is_name_implicit, 'icon': icon})

    async def edit_forum_topic(self, chat_id: int = None, forum_topic_id: int = None, name: str = None, edit_icon_custom_emoji: bool = None, icon_custom_emoji_id: int = None) -> Ok:
        """
        description Edits title and icon of a topic in a forum supergroup chat or a chat with a bot with topics; for supergroup chats requires can_manage_topics administrator right
        chat_id Identifier of the chat
        forum_topic_id Forum topic identifier
        name New name of the topic; 0-128 characters. If empty, the previous topic name is kept
        edit_icon_custom_emoji Pass true to edit the icon of the topic. Icon of the General topic can't be edited
        icon_custom_emoji_id Identifier of the new custom emoji for topic icon; pass 0 to remove the custom emoji. Ignored if edit_icon_custom_emoji is false. Telegram Premium users can use any custom emoji, other users can use only a custom emoji returned by getForumTopicDefaultIcons
        """
        return await self._client.call_method('editForumTopic', {'@type': 'editForumTopic', 'chat_id': chat_id, 'forum_topic_id': forum_topic_id, 'name': name, 'edit_icon_custom_emoji': edit_icon_custom_emoji, 'icon_custom_emoji_id': icon_custom_emoji_id})

    async def get_forum_topic(self, chat_id: int = None, forum_topic_id: int = None) -> ForumTopic:
        """
        description Returns information about a topic in a forum supergroup chat or a chat with a bot with topics
        chat_id Identifier of the chat
        forum_topic_id Forum topic identifier
        """
        return await self._client.call_method('getForumTopic', {'@type': 'getForumTopic', 'chat_id': chat_id, 'forum_topic_id': forum_topic_id})

    async def get_forum_topic_history(self, chat_id: int = None, forum_topic_id: int = None, from_message_id: int = None, offset: int = None, limit: int = None) -> Messages:
        """
        description Returns messages in a topic in a forum supergroup chat or a chat with a bot with topics. The messages are returned in reverse chronological order
        chat_id Chat identifier
        forum_topic_id Forum topic identifier
        from_message_id Identifier of the message starting from which history must be fetched; use 0 to get results from the last message
        offset Specify 0 to get results from exactly the message from_message_id or a negative number from -99 to -1 to get additionally -offset newer messages
        limit The maximum number of messages to be returned; must be positive and can't be greater than 100. If the offset is negative, then the limit must be greater than or equal to -offset.
        """
        return await self._client.call_method('getForumTopicHistory', {'@type': 'getForumTopicHistory', 'chat_id': chat_id, 'forum_topic_id': forum_topic_id, 'from_message_id': from_message_id, 'offset': offset, 'limit': limit})

    async def get_forum_topic_link(self, chat_id: int = None, forum_topic_id: int = None) -> MessageLink:
        """
        description Returns an HTTPS link to a topic in a forum supergroup chat. This is an offline method @chat_id Identifier of the chat @forum_topic_id Forum topic identifier
        """
        return await self._client.call_method('getForumTopicLink', {'@type': 'getForumTopicLink', 'chat_id': chat_id, 'forum_topic_id': forum_topic_id})

    async def get_forum_topics(self, chat_id: int = None, query: str = None, offset_date: int = None, offset_message_id: int = None, offset_forum_topic_id: int = None, limit: int = None) -> ForumTopics:
        """
        description Returns found forum topics in a forum supergroup chat or a chat with a bot with topics. This is a temporary method for getting information about topic list from the server
        chat_id Identifier of the chat
        query Query to search for in the forum topic's name
        offset_date The date starting from which the results need to be fetched. Use 0 or any date in the future to get results from the last topic
        offset_message_id The message identifier of the last message in the last found topic, or 0 for the first request
        offset_forum_topic_id The forum topic identifier of the last found topic, or 0 for the first request
        limit The maximum number of forum topics to be returned; up to 100. For optimal performance, the number of returned forum topics is chosen by TDLib and can be smaller than the specified limit
        """
        return await self._client.call_method('getForumTopics', {'@type': 'getForumTopics', 'chat_id': chat_id, 'query': query, 'offset_date': offset_date, 'offset_message_id': offset_message_id, 'offset_forum_topic_id': offset_forum_topic_id, 'limit': limit})

    async def set_forum_topic_notification_settings(self, chat_id: int = None, forum_topic_id: int = None, notification_settings: chatNotificationSettings = None) -> Ok:
        """
        description Changes the notification settings of a forum topic in a forum supergroup chat or a chat with a bot with topics
        chat_id Chat identifier
        forum_topic_id Forum topic identifier
        notification_settings New notification settings for the forum topic. If the topic is muted for more than 366 days, it is considered to be muted forever
        """
        return await self._client.call_method('setForumTopicNotificationSettings', {'@type': 'setForumTopicNotificationSettings', 'chat_id': chat_id, 'forum_topic_id': forum_topic_id, 'notification_settings': notification_settings})

    async def toggle_forum_topic_is_closed(self, chat_id: int = None, forum_topic_id: int = None, is_closed: bool = None) -> Ok:
        """
        description Toggles whether a topic is closed in a forum supergroup chat; requires can_manage_topics administrator right in the supergroup unless the user is creator of the topic
        chat_id Identifier of the chat
        forum_topic_id Forum topic identifier
        is_closed Pass true to close the topic; pass false to reopen it
        """
        return await self._client.call_method('toggleForumTopicIsClosed', {'@type': 'toggleForumTopicIsClosed', 'chat_id': chat_id, 'forum_topic_id': forum_topic_id, 'is_closed': is_closed})

    async def toggle_general_forum_topic_is_hidden(self, chat_id: int = None, is_hidden: bool = None) -> Ok:
        """
        description Toggles whether a General topic is hidden in a forum supergroup chat; requires can_manage_topics administrator right in the supergroup
        chat_id Identifier of the chat
        is_hidden Pass true to hide and close the General topic; pass false to unhide it
        """
        return await self._client.call_method('toggleGeneralForumTopicIsHidden', {'@type': 'toggleGeneralForumTopicIsHidden', 'chat_id': chat_id, 'is_hidden': is_hidden})

    async def toggle_forum_topic_is_pinned(self, chat_id: int = None, forum_topic_id: int = None, is_pinned: bool = None) -> Ok:
        """
        description Changes the pinned state of a topic in a forum supergroup chat or a chat with a bot with topics; requires can_manage_topics administrator right in the supergroup.
        chat_id Chat identifier
        forum_topic_id Forum topic identifier
        is_pinned Pass true to pin the topic; pass false to unpin it
        """
        return await self._client.call_method('toggleForumTopicIsPinned', {'@type': 'toggleForumTopicIsPinned', 'chat_id': chat_id, 'forum_topic_id': forum_topic_id, 'is_pinned': is_pinned})

    async def set_pinned_forum_topics(self, chat_id: int = None, forum_topic_ids: List[int] = None) -> Ok:
        """
        description Changes the order of pinned topics in a forum supergroup chat or a chat with a bot with topics; requires can_manage_topics administrator right in the supergroup
        chat_id Chat identifier
        forum_topic_ids The new list of identifiers of the pinned forum topics
        """
        return await self._client.call_method('setPinnedForumTopics', {'@type': 'setPinnedForumTopics', 'chat_id': chat_id, 'forum_topic_ids': forum_topic_ids})

    async def delete_forum_topic(self, chat_id: int = None, forum_topic_id: int = None) -> Ok:
        """
        description Deletes all messages from a topic in a forum supergroup chat or a chat with a bot with topics; requires can_delete_messages administrator right in the supergroup
        chat_id Identifier of the chat
        forum_topic_id Forum topic identifier
        """
        return await self._client.call_method('deleteForumTopic', {'@type': 'deleteForumTopic', 'chat_id': chat_id, 'forum_topic_id': forum_topic_id})

    async def read_all_forum_topic_mentions(self, chat_id: int = None, forum_topic_id: int = None) -> Ok:
        """
        description Marks all mentions in a topic in a forum supergroup chat as read
        chat_id Chat identifier
        forum_topic_id Forum topic identifier in which mentions are marked as read
        """
        return await self._client.call_method('readAllForumTopicMentions', {'@type': 'readAllForumTopicMentions', 'chat_id': chat_id, 'forum_topic_id': forum_topic_id})

    async def read_all_forum_topic_reactions(self, chat_id: int = None, forum_topic_id: int = None) -> Ok:
        """
        description Marks all reactions in a topic in a forum supergroup chat or a chat with a bot with topics as read
        chat_id Chat identifier
        forum_topic_id Forum topic identifier in which reactions are marked as read
        """
        return await self._client.call_method('readAllForumTopicReactions', {'@type': 'readAllForumTopicReactions', 'chat_id': chat_id, 'forum_topic_id': forum_topic_id})

    async def read_all_forum_topic_poll_votes(self, chat_id: int = None, forum_topic_id: int = None) -> Ok:
        """
        description Marks all poll votes in a topic in a forum supergroup chat as read
        chat_id Chat identifier
        forum_topic_id Forum topic identifier in which poll votes are marked as read
        """
        return await self._client.call_method('readAllForumTopicPollVotes', {'@type': 'readAllForumTopicPollVotes', 'chat_id': chat_id, 'forum_topic_id': forum_topic_id})

    async def unpin_all_forum_topic_messages(self, chat_id: int = None, forum_topic_id: int = None) -> Ok:
        """
        description Removes all pinned messages from a topic in a forum supergroup chat or a chat with a bot with topics; requires can_pin_messages member right in the supergroup
        chat_id Identifier of the chat
        forum_topic_id Forum topic identifier in which messages will be unpinned
        """
        return await self._client.call_method('unpinAllForumTopicMessages', {'@type': 'unpinAllForumTopicMessages', 'chat_id': chat_id, 'forum_topic_id': forum_topic_id})

    async def get_passkey_parameters(self) -> Text:
        """
        description Returns parameters for creating of a new passkey as JSON-serialized string
        """
        return await self._client.call_method('getPasskeyParameters', {'@type': 'getPasskeyParameters'})

    async def add_login_passkey(self, client_data: str = None, attestation_object: bytes = None) -> Passkey:
        """
        description Adds a passkey allowed to be used for the login by the current user and returns the added passkey. Call getPasskeyParameters to get parameters for creating of the passkey
        client_data JSON-encoded client data
        attestation_object Passkey attestation object
        """
        return await self._client.call_method('addLoginPasskey', {'@type': 'addLoginPasskey', 'client_data': client_data, 'attestation_object': attestation_object})

    async def get_login_passkeys(self) -> Passkeys:
        """
        description Returns the list of passkeys allowed to be used for the login by the current user
        """
        return await self._client.call_method('getLoginPasskeys', {'@type': 'getLoginPasskeys'})

    async def remove_login_passkey(self, passkey_id: str = None) -> Ok:
        """
        description Removes a passkey from the list of passkeys allowed to be used for the login by the current user @passkey_id Unique identifier of the passkey to remove
        """
        return await self._client.call_method('removeLoginPasskey', {'@type': 'removeLoginPasskey', 'passkey_id': passkey_id})

    async def get_emoji_reaction(self, emoji: str = None) -> EmojiReaction:
        """
        description Returns information about an emoji reaction. Returns a 404 error if the reaction is not found @emoji Text representation of the reaction
        """
        return await self._client.call_method('getEmojiReaction', {'@type': 'getEmojiReaction', 'emoji': emoji})

    async def get_custom_emoji_reaction_animations(self) -> Stickers:
        """
        description Returns TGS stickers with generic animations for custom emoji reactions
        """
        return await self._client.call_method('getCustomEmojiReactionAnimations', {'@type': 'getCustomEmojiReactionAnimations'})

    async def get_message_available_reactions(self, chat_id: int = None, message_id: int = None, row_size: int = None) -> AvailableReactions:
        """
        description Returns reactions, which can be added to a message. The list can change after updateActiveEmojiReactions, updateChatAvailableReactions for the chat, or updateMessageInteractionInfo for the message
        chat_id Identifier of the chat to which the message belongs
        message_id Identifier of the message
        row_size Number of reaction per row, 5-25
        """
        return await self._client.call_method('getMessageAvailableReactions', {'@type': 'getMessageAvailableReactions', 'chat_id': chat_id, 'message_id': message_id, 'row_size': row_size})

    async def clear_recent_reactions(self) -> Ok:
        """
        description Clears the list of recently used reactions
        """
        return await self._client.call_method('clearRecentReactions', {'@type': 'clearRecentReactions'})

    async def add_message_reaction(self, chat_id: int = None, message_id: int = None, reaction_type: ReactionType = None, is_big: bool = None, update_recent_reactions: bool = None) -> Ok:
        """
        description Adds a reaction or a tag to a message. Use getMessageAvailableReactions to receive the list of available reactions for the message
        chat_id Identifier of the chat to which the message belongs
        message_id Identifier of the message
        reaction_type Type of the reaction to add. Use addPendingPaidMessageReaction instead to add the paid reaction
        is_big Pass true if the reaction is added with a big animation
        update_recent_reactions Pass true if the reaction needs to be added to recent reactions; tags are never added to the list of recent reactions
        """
        return await self._client.call_method('addMessageReaction', {'@type': 'addMessageReaction', 'chat_id': chat_id, 'message_id': message_id, 'reaction_type': reaction_type, 'is_big': is_big, 'update_recent_reactions': update_recent_reactions})

    async def remove_message_reaction(self, chat_id: int = None, message_id: int = None, reaction_type: ReactionType = None) -> Ok:
        """
        description Removes a reaction from a message. A chosen reaction can always be removed
        chat_id Identifier of the chat to which the message belongs
        message_id Identifier of the message
        reaction_type Type of the reaction to remove. The paid reaction can't be removed
        """
        return await self._client.call_method('removeMessageReaction', {'@type': 'removeMessageReaction', 'chat_id': chat_id, 'message_id': message_id, 'reaction_type': reaction_type})

    async def delete_all_recent_message_reactions_from_sender(self, chat_id: int = None, sender_id: MessageSender = None) -> Ok:
        """
        description Deletes all recent reactions added by the specified sender in a chat. Supported only for basic groups and supergroups; requires can_delete_messages administrator right
        chat_id Chat identifier
        sender_id Identifier of the sender of reactions to delete
        """
        return await self._client.call_method('deleteAllRecentMessageReactionsFromSender', {'@type': 'deleteAllRecentMessageReactionsFromSender', 'chat_id': chat_id, 'sender_id': sender_id})

    async def delete_message_reactions_from_sender(self, chat_id: int = None, message_id: int = None, sender_id: MessageSender = None) -> Ok:
        """
        description Deletes all reactions added by the specified sender on a message
        chat_id Chat identifier
        message_id Identifier of the message containing the reactions. Use messageProperties.can_delete_reactions to check whether the method can be used for a message
        sender_id Identifier of the sender of reactions to delete
        """
        return await self._client.call_method('deleteMessageReactionsFromSender', {'@type': 'deleteMessageReactionsFromSender', 'chat_id': chat_id, 'message_id': message_id, 'sender_id': sender_id})

    async def get_chat_available_paid_message_reaction_senders(self, chat_id: int = None) -> MessageSenders:
        """
        description Returns the list of message sender identifiers, which can be used to send a paid reaction in a chat @chat_id Chat identifier
        """
        return await self._client.call_method('getChatAvailablePaidMessageReactionSenders', {'@type': 'getChatAvailablePaidMessageReactionSenders', 'chat_id': chat_id})

    async def add_pending_paid_message_reaction(self, chat_id: int = None, message_id: int = None, star_count: int = None, type: PaidReactionType = None) -> Ok:
        """
        description Adds the paid message reaction to a message. Use getMessageAvailableReactions to check whether the reaction is available for the message
        chat_id Identifier of the chat to which the message belongs
        message_id Identifier of the message
        star_count Number of Telegram Stars to be used for the reaction. The total number of pending paid reactions must not exceed getOption("paid_reaction_star_count_max")
        type Type of the paid reaction; pass null if the user didn't choose reaction type explicitly, for example, the reaction is set from the message bubble
        """
        return await self._client.call_method('addPendingPaidMessageReaction', {'@type': 'addPendingPaidMessageReaction', 'chat_id': chat_id, 'message_id': message_id, 'star_count': star_count, 'type': type})

    async def commit_pending_paid_message_reactions(self, chat_id: int = None, message_id: int = None) -> Ok:
        """
        description Applies all pending paid reactions on a message @chat_id Identifier of the chat to which the message belongs @message_id Identifier of the message
        """
        return await self._client.call_method('commitPendingPaidMessageReactions', {'@type': 'commitPendingPaidMessageReactions', 'chat_id': chat_id, 'message_id': message_id})

    async def remove_pending_paid_message_reactions(self, chat_id: int = None, message_id: int = None) -> Ok:
        """
        description Removes all pending paid reactions on a message @chat_id Identifier of the chat to which the message belongs @message_id Identifier of the message
        """
        return await self._client.call_method('removePendingPaidMessageReactions', {'@type': 'removePendingPaidMessageReactions', 'chat_id': chat_id, 'message_id': message_id})

    async def set_paid_message_reaction_type(self, chat_id: int = None, message_id: int = None, type: PaidReactionType = None) -> Ok:
        """
        description Changes type of paid message reaction of the current user on a message. The message must have paid reaction added by the current user
        chat_id Identifier of the chat to which the message belongs
        message_id Identifier of the message
        type New type of the paid reaction
        """
        return await self._client.call_method('setPaidMessageReactionType', {'@type': 'setPaidMessageReactionType', 'chat_id': chat_id, 'message_id': message_id, 'type': type})

    async def set_message_reactions(self, chat_id: int = None, message_id: int = None, reaction_types: List[ReactionType] = None, is_big: bool = None) -> Ok:
        """
        description Sets reactions on a message; for bots only
        chat_id Identifier of the chat to which the message belongs
        message_id Identifier of the message
        reaction_types Types of the reaction to set; pass an empty list to remove the reactions
        is_big Pass true if the reactions are added with a big animation
        """
        return await self._client.call_method('setMessageReactions', {'@type': 'setMessageReactions', 'chat_id': chat_id, 'message_id': message_id, 'reaction_types': reaction_types, 'is_big': is_big})

    async def get_message_added_reactions(self, chat_id: int = None, message_id: int = None, reaction_type: ReactionType = None, offset: str = None, limit: int = None) -> AddedReactions:
        """
        description Returns reactions added for a message, along with their sender
        chat_id Identifier of the chat to which the message belongs
        message_id Identifier of the message. Use message.interaction_info.reactions.can_get_added_reactions to check whether added reactions can be received for the message
        reaction_type Type of the reactions to return; pass null to return all added reactions; reactionTypePaid isn't supported
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of reactions to be returned; must be positive and can't be greater than 100
        """
        return await self._client.call_method('getMessageAddedReactions', {'@type': 'getMessageAddedReactions', 'chat_id': chat_id, 'message_id': message_id, 'reaction_type': reaction_type, 'offset': offset, 'limit': limit})

    async def set_default_reaction_type(self, reaction_type: ReactionType = None) -> Ok:
        """
        description Changes type of default reaction for the current user @reaction_type New type of the default reaction. The paid reaction can't be set as default
        """
        return await self._client.call_method('setDefaultReactionType', {'@type': 'setDefaultReactionType', 'reaction_type': reaction_type})

    async def get_saved_messages_tags(self, saved_messages_topic_id: int = None) -> SavedMessagesTags:
        """
        description Returns tags used in Saved Messages or a Saved Messages topic
        saved_messages_topic_id Identifier of Saved Messages topic which tags will be returned; pass 0 to get all Saved Messages tags
        """
        return await self._client.call_method('getSavedMessagesTags', {'@type': 'getSavedMessagesTags', 'saved_messages_topic_id': saved_messages_topic_id})

    async def set_saved_messages_tag_label(self, tag: ReactionType = None, label: str = None) -> Ok:
        """
        description Changes label of a Saved Messages tag; for Telegram Premium users only @tag The tag which label will be changed @label New label for the tag; 0-12 characters
        """
        return await self._client.call_method('setSavedMessagesTagLabel', {'@type': 'setSavedMessagesTagLabel', 'tag': tag, 'label': label})

    async def get_message_effect(self, effect_id: int = None) -> MessageEffect:
        """
        description Returns information about a message effect. Returns a 404 error if the effect is not found @effect_id Unique identifier of the effect
        """
        return await self._client.call_method('getMessageEffect', {'@type': 'getMessageEffect', 'effect_id': effect_id})

    async def search_quote(self, text: formattedText = None, quote: formattedText = None, quote_position: int = None) -> FoundPosition:
        """
        description Searches for a given quote in a text. Returns found quote start position in UTF-16 code units. Returns a 404 error if the quote is not found. Can be called synchronously
        text Text in which to search for the quote
        quote Quote to search for
        quote_position Approximate quote position in UTF-16 code units
        """
        return await self._client.call_method('searchQuote', {'@type': 'searchQuote', 'text': text, 'quote': quote, 'quote_position': quote_position})

    async def get_text_entities(self, text: str = None) -> TextEntities:
        """
        description Returns all entities (mentions, hashtags, cashtags, bot commands, bank card numbers, URLs, and email addresses) found in the text. Can be called synchronously @text The text in which to look for entities
        """
        return await self._client.call_method('getTextEntities', {'@type': 'getTextEntities', 'text': text})

    async def parse_text_entities(self, text: str = None, parse_mode: TextParseMode = None) -> FormattedText:
        """
        description Parses Bold, Italic, Underline, Strikethrough, Spoiler, CustomEmoji, BlockQuote, ExpandableBlockQuote, Code, Pre, PreCode, TextUrl,
        text The text to parse
        parse_mode Text parse mode
        """
        return await self._client.call_method('parseTextEntities', {'@type': 'parseTextEntities', 'text': text, 'parse_mode': parse_mode})

    async def parse_markdown(self, text: formattedText = None) -> FormattedText:
        """
        description Parses Markdown entities in a human-friendly format, ignoring markup errors. Can be called synchronously
        text The text to parse. For example, "__italic__ ~~strikethrough~~ ||spoiler|| **bold** `code` ```pre``` __[italic__ text_url](telegram.org) __italic**bold italic__bold**"
        """
        return await self._client.call_method('parseMarkdown', {'@type': 'parseMarkdown', 'text': text})

    async def get_markdown_text(self, text: formattedText = None) -> FormattedText:
        """
        description Replaces text entities with Markdown formatting in a human-friendly format. Entities that can't be represented in Markdown unambiguously are kept as is. Can be called synchronously @text The text
        """
        return await self._client.call_method('getMarkdownText', {'@type': 'getMarkdownText', 'text': text})

    async def get_country_flag_emoji(self, country_code: str = None) -> Text:
        """
        description Returns an emoji for the given country. Returns an empty string on failure. Can be called synchronously @country_code A two-letter ISO 3166-1 alpha-2 country code as received from getCountries
        """
        return await self._client.call_method('getCountryFlagEmoji', {'@type': 'getCountryFlagEmoji', 'country_code': country_code})

    async def get_file_mime_type(self, file_name: str = None) -> Text:
        """
        description Returns the MIME type of a file, guessed by its extension. Returns an empty string on failure. Can be called synchronously @file_name The name of the file or path to the file
        """
        return await self._client.call_method('getFileMimeType', {'@type': 'getFileMimeType', 'file_name': file_name})

    async def get_file_extension(self, mime_type: str = None) -> Text:
        """
        description Returns the extension of a file, guessed by its MIME type. Returns an empty string on failure. Can be called synchronously @mime_type The MIME type of the file
        """
        return await self._client.call_method('getFileExtension', {'@type': 'getFileExtension', 'mime_type': mime_type})

    async def clean_file_name(self, file_name: str = None) -> Text:
        """
        description Removes potentially dangerous characters from the name of a file. Returns an empty string on failure. Can be called synchronously @file_name File name or path to the file
        """
        return await self._client.call_method('cleanFileName', {'@type': 'cleanFileName', 'file_name': file_name})

    async def get_language_pack_string(self, language_pack_database_path: str = None, localization_target: str = None, language_pack_id: str = None, key: str = None) -> LanguagePackStringValue:
        """
        description Returns a string stored in the local database from the specified localization target and language pack by its key. Returns a 404 error if the string is not found. Can be called synchronously
        language_pack_database_path Path to the language pack database in which strings are stored
        localization_target Localization target to which the language pack belongs
        language_pack_id Language pack identifier
        key Language pack key of the string to be returned
        """
        return await self._client.call_method('getLanguagePackString', {'@type': 'getLanguagePackString', 'language_pack_database_path': language_pack_database_path, 'localization_target': localization_target, 'language_pack_id': language_pack_id, 'key': key})

    async def get_json_value(self, json: str = None) -> JsonValue:
        """
        description Converts a JSON-serialized string to corresponding JsonValue object. Can be called synchronously @json The JSON-serialized string
        """
        return await self._client.call_method('getJsonValue', {'@type': 'getJsonValue', 'json': json})

    async def get_json_string(self, json_value: JsonValue = None) -> Text:
        """
        description Converts a JsonValue object to corresponding JSON-serialized string. Can be called synchronously @json_value The JsonValue object
        """
        return await self._client.call_method('getJsonString', {'@type': 'getJsonString', 'json_value': json_value})

    async def get_theme_parameters_json_string(self, theme: themeParameters = None) -> Text:
        """
        description Converts a themeParameters object to corresponding JSON-serialized string. Can be called synchronously @theme Theme parameters to convert to JSON
        """
        return await self._client.call_method('getThemeParametersJsonString', {'@type': 'getThemeParametersJsonString', 'theme': theme})

    async def add_poll_option(self, chat_id: int = None, message_id: int = None, option: inputPollOption = None) -> Ok:
        """
        description Adds an option to a poll
        chat_id Identifier of the chat to which the poll belongs
        message_id Identifier of the message containing the poll. Use messagePoll.can_add_option to check whether an option can be added
        option The new option
        """
        return await self._client.call_method('addPollOption', {'@type': 'addPollOption', 'chat_id': chat_id, 'message_id': message_id, 'option': option})

    async def delete_poll_option(self, chat_id: int = None, message_id: int = None, option_id: str = None) -> Ok:
        """
        description Deletes an option from a poll
        chat_id Identifier of the chat to which the poll belongs
        message_id Identifier of the message containing the poll
        option_id Unique identifier of the option. Use pollOptionProperties.can_be_deleted to check whether the option can be deleted by the user
        """
        return await self._client.call_method('deletePollOption', {'@type': 'deletePollOption', 'chat_id': chat_id, 'message_id': message_id, 'option_id': option_id})

    async def set_poll_answer(self, chat_id: int = None, message_id: int = None, option_ids: List[int] = None) -> Ok:
        """
        description Changes the user answer to a poll
        chat_id Identifier of the chat to which the poll belongs
        message_id Identifier of the message containing the poll
        option_ids 0-based identifiers of answer options, chosen by the user. User can choose more than 1 answer option only is the poll allows multiple answers
        """
        return await self._client.call_method('setPollAnswer', {'@type': 'setPollAnswer', 'chat_id': chat_id, 'message_id': message_id, 'option_ids': option_ids})

    async def get_poll_voters(self, chat_id: int = None, message_id: int = None, option_id: int = None, offset: int = None, limit: int = None) -> PollVoters:
        """
        description Returns message senders voted for the specified option in a poll; use poll.can_get_voters to check whether the method can be used.
        chat_id Identifier of the chat to which the poll belongs
        message_id Identifier of the message containing the poll
        option_id 0-based identifier of the answer option
        offset Number of voters to skip in the result; must be non-negative
        limit The maximum number of voters to be returned; must be positive and can't be greater than 50. For optimal performance, the number of returned voters is chosen by TDLib and can be smaller than the specified limit, even if the end of the voter list has not been reached
        """
        return await self._client.call_method('getPollVoters', {'@type': 'getPollVoters', 'chat_id': chat_id, 'message_id': message_id, 'option_id': option_id, 'offset': offset, 'limit': limit})

    async def get_poll_vote_statistics(self, chat_id: int = None, message_id: int = None, is_dark: bool = None) -> PollVoteStatistics:
        """
        description Returns statistics of poll votes in a poll
        chat_id Identifier of the chat to which the poll belongs
        message_id Identifier of the message containing the poll. Use messageProperties.can_get_poll_vote_statistics to check whether the method can be used for a message
        is_dark Pass true if a dark theme is used by the application
        """
        return await self._client.call_method('getPollVoteStatistics', {'@type': 'getPollVoteStatistics', 'chat_id': chat_id, 'message_id': message_id, 'is_dark': is_dark})

    async def stop_poll(self, chat_id: int = None, message_id: int = None, reply_markup: ReplyMarkup = None) -> Ok:
        """
        description Stops a poll
        chat_id Identifier of the chat to which the poll belongs
        message_id Identifier of the message containing the poll. Use messageProperties.can_be_edited to check whether the poll can be stopped
        reply_markup The new message reply markup; pass null if none; for bots only
        """
        return await self._client.call_method('stopPoll', {'@type': 'stopPoll', 'chat_id': chat_id, 'message_id': message_id, 'reply_markup': reply_markup})

    async def add_checklist_tasks(self, chat_id: int = None, message_id: int = None, tasks: List[inputChecklistTask] = None) -> Ok:
        """
        description Adds tasks to a checklist in a message
        chat_id Identifier of the chat with the message
        message_id Identifier of the message containing the checklist. Use messageProperties.can_add_tasks to check whether the tasks can be added
        tasks List of added tasks
        """
        return await self._client.call_method('addChecklistTasks', {'@type': 'addChecklistTasks', 'chat_id': chat_id, 'message_id': message_id, 'tasks': tasks})

    async def mark_checklist_tasks_as_done(self, chat_id: int = None, message_id: int = None, marked_as_done_task_ids: List[int] = None, marked_as_not_done_task_ids: List[int] = None) -> Ok:
        """
        description Adds tasks of a checklist in a message as done or not done
        chat_id Identifier of the chat with the message
        message_id Identifier of the message containing the checklist. Use messageProperties.can_mark_tasks_as_done to check whether the tasks can be marked as done or not done
        marked_as_done_task_ids Identifiers of tasks that were marked as done
        marked_as_not_done_task_ids Identifiers of tasks that were marked as not done
        """
        return await self._client.call_method('markChecklistTasksAsDone', {'@type': 'markChecklistTasksAsDone', 'chat_id': chat_id, 'message_id': message_id, 'marked_as_done_task_ids': marked_as_done_task_ids, 'marked_as_not_done_task_ids': marked_as_not_done_task_ids})

    async def hide_suggested_action(self, action: SuggestedAction = None) -> Ok:
        """
        description Hides a suggested action @action Suggested action to hide
        """
        return await self._client.call_method('hideSuggestedAction', {'@type': 'hideSuggestedAction', 'action': action})

    async def hide_contact_close_birthdays(self) -> Ok:
        """
        description Hides the list of contacts that have close birthdays for 24 hours
        """
        return await self._client.call_method('hideContactCloseBirthdays', {'@type': 'hideContactCloseBirthdays'})

    async def get_business_connection(self, connection_id: str = None) -> BusinessConnection:
        """
        description Returns information about a business connection by its identifier; for bots only @connection_id Identifier of the business connection to return
        """
        return await self._client.call_method('getBusinessConnection', {'@type': 'getBusinessConnection', 'connection_id': connection_id})

    async def get_login_url_info(self, chat_id: int = None, message_id: int = None, button_id: int = None) -> LoginUrlInfo:
        """
        description Returns information about a button of type inlineKeyboardButtonTypeLoginUrl. The method needs to be called when the user presses the button
        chat_id Chat identifier of the message with the button
        message_id Message identifier of the message with the button. The message must not be scheduled
        button_id Button identifier
        """
        return await self._client.call_method('getLoginUrlInfo', {'@type': 'getLoginUrlInfo', 'chat_id': chat_id, 'message_id': message_id, 'button_id': button_id})

    async def get_login_url(self, chat_id: int = None, message_id: int = None, button_id: int = None, allow_write_access: bool = None) -> HttpUrl:
        """
        description Returns an HTTP URL which can be used to automatically authorize the user on a website after clicking an inline button of type inlineKeyboardButtonTypeLoginUrl.
        chat_id Chat identifier of the message with the button
        message_id Message identifier of the message with the button
        button_id Button identifier
        allow_write_access Pass true to allow the bot to send messages to the current user. Phone number access can't be requested using the button
        """
        return await self._client.call_method('getLoginUrl', {'@type': 'getLoginUrl', 'chat_id': chat_id, 'message_id': message_id, 'button_id': button_id, 'allow_write_access': allow_write_access})

    async def share_users_with_bot(self, source: KeyboardButtonSource = None, button_id: int = None, shared_user_ids: List[int] = None, only_check: bool = None) -> Ok:
        """
        description Shares users after pressing a keyboardButtonTypeRequestUsers button with the bot
        source Source of the button
        button_id Identifier of the button
        shared_user_ids Identifiers of the shared users
        only_check Pass true to check that the users can be shared by the button instead of actually sharing them
        """
        return await self._client.call_method('shareUsersWithBot', {'@type': 'shareUsersWithBot', 'source': source, 'button_id': button_id, 'shared_user_ids': shared_user_ids, 'only_check': only_check})

    async def share_chat_with_bot(self, source: KeyboardButtonSource = None, button_id: int = None, shared_chat_id: int = None, only_check: bool = None) -> Ok:
        """
        description Shares a chat after pressing a keyboardButtonTypeRequestChat button with the bot
        source Source of the button
        button_id Identifier of the button
        shared_chat_id Identifier of the shared chat
        only_check Pass true to check that the chat can be shared by the button instead of actually sharing it. Doesn't check bot_is_member and bot_administrator_rights restrictions.
        """
        return await self._client.call_method('shareChatWithBot', {'@type': 'shareChatWithBot', 'source': source, 'button_id': button_id, 'shared_chat_id': shared_chat_id, 'only_check': only_check})

    async def get_inline_query_results(self, bot_user_id: int = None, chat_id: int = None, user_location: location = None, query: str = None, offset: str = None) -> InlineQueryResults:
        """
        description Sends an inline query to a bot and returns its results. Returns an error with code 502 if the bot fails to answer the query before the query timeout expires
        bot_user_id Identifier of the target bot
        chat_id Identifier of the chat where the query was sent
        user_location Location of the user; pass null if unknown or the bot doesn't need user's location
        query Text of the query
        offset Offset of the first entry to return; use empty string to get the first chunk of results
        """
        return await self._client.call_method('getInlineQueryResults', {'@type': 'getInlineQueryResults', 'bot_user_id': bot_user_id, 'chat_id': chat_id, 'user_location': user_location, 'query': query, 'offset': offset})

    async def answer_inline_query(self, inline_query_id: int = None, is_personal: bool = None, button: inlineQueryResultsButton = None, results: List[InputInlineQueryResult] = None, cache_time: int = None, next_offset: str = None) -> Ok:
        """
        description Sets the result of an inline query; for bots only
        inline_query_id Identifier of the inline query
        is_personal Pass true if results may be cached and returned only for the user who sent the query. By default, results may be returned to any user who sends the same query
        button Button to be shown above inline query results; pass null if none
        results The results of the query
        cache_time Allowed time to cache the results of the query, in seconds
        next_offset Offset for the next inline query; pass an empty string if there are no more results
        """
        return await self._client.call_method('answerInlineQuery', {'@type': 'answerInlineQuery', 'inline_query_id': inline_query_id, 'is_personal': is_personal, 'button': button, 'results': results, 'cache_time': cache_time, 'next_offset': next_offset})

    async def answer_guest_query(self, guest_query_id: int = None, result: InputInlineQueryResult = None) -> InlineMessageId:
        """
        description Sets the result of a guest query; for bots only
        guest_query_id Identifier of the guest query
        result The result of the query
        """
        return await self._client.call_method('answerGuestQuery', {'@type': 'answerGuestQuery', 'guest_query_id': guest_query_id, 'result': result})

    async def save_prepared_inline_message(self, user_id: int = None, result: InputInlineQueryResult = None, chat_types: targetChatTypes = None) -> PreparedInlineMessageId:
        """
        description Saves an inline message to be sent by the given user; for bots only
        user_id Identifier of the user
        result The description of the message
        chat_types Types of the chats to which the message can be sent
        """
        return await self._client.call_method('savePreparedInlineMessage', {'@type': 'savePreparedInlineMessage', 'user_id': user_id, 'result': result, 'chat_types': chat_types})

    async def get_prepared_inline_message(self, bot_user_id: int = None, prepared_message_id: str = None) -> PreparedInlineMessage:
        """
        description Saves an inline message to be sent by the given user
        bot_user_id Identifier of the bot that created the message
        prepared_message_id Identifier of the prepared message
        """
        return await self._client.call_method('getPreparedInlineMessage', {'@type': 'getPreparedInlineMessage', 'bot_user_id': bot_user_id, 'prepared_message_id': prepared_message_id})

    async def save_prepared_keyboard_button(self, user_id: int = None, button: keyboardButton = None) -> Text:
        """
        description Saves a keyboard button to be shown to the given user; for bots only
        user_id Identifier of the user
        button The button; must be of the type keyboardButtonTypeRequestUsers, keyboardButtonTypeRequestChat, or keyboardButtonTypeRequestManagedBot
        """
        return await self._client.call_method('savePreparedKeyboardButton', {'@type': 'savePreparedKeyboardButton', 'user_id': user_id, 'button': button})

    async def get_prepared_keyboard_button(self, bot_user_id: int = None, prepared_button_id: str = None) -> KeyboardButton:
        """
        description Returns a keyboard button prepared by the bot for the user. The button will be of the type keyboardButtonTypeRequestUsers, keyboardButtonTypeRequestChat, or keyboardButtonTypeRequestManagedBot
        bot_user_id Identifier of the bot that created the button
        prepared_button_id Identifier of the prepared button
        """
        return await self._client.call_method('getPreparedKeyboardButton', {'@type': 'getPreparedKeyboardButton', 'bot_user_id': bot_user_id, 'prepared_button_id': prepared_button_id})

    async def get_grossing_web_app_bots(self, offset: str = None, limit: int = None) -> FoundUsers:
        """
        description Returns the most grossing Web App bots
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of bots to be returned; up to 100
        """
        return await self._client.call_method('getGrossingWebAppBots', {'@type': 'getGrossingWebAppBots', 'offset': offset, 'limit': limit})

    async def search_web_app(self, bot_user_id: int = None, web_app_short_name: str = None) -> FoundWebApp:
        """
        description Returns information about a Web App by its short name. Returns a 404 error if the Web App is not found
        bot_user_id Identifier of the target bot
        web_app_short_name Short name of the Web App
        """
        return await self._client.call_method('searchWebApp', {'@type': 'searchWebApp', 'bot_user_id': bot_user_id, 'web_app_short_name': web_app_short_name})

    async def get_web_app_placeholder(self, bot_user_id: int = None) -> Outline:
        """
        description Returns a default placeholder for Web Apps of a bot. This is an offline method. Returns a 404 error if the placeholder isn't known @bot_user_id Identifier of the target bot
        """
        return await self._client.call_method('getWebAppPlaceholder', {'@type': 'getWebAppPlaceholder', 'bot_user_id': bot_user_id})

    async def get_web_app_link_url(self, chat_id: int = None, bot_user_id: int = None, web_app_short_name: str = None, start_parameter: str = None, allow_write_access: bool = None, parameters: webAppOpenParameters = None) -> WebAppUrl:
        """
        description Returns an HTTPS URL of a Web App to open after a link of the type internalLinkTypeWebApp is clicked
        chat_id Identifier of the chat in which the link was clicked; pass 0 if none
        bot_user_id Identifier of the target bot
        web_app_short_name Short name of the Web App
        start_parameter Start parameter from internalLinkTypeWebApp
        allow_write_access Pass true if the current user allowed the bot to send them messages
        parameters Parameters to use to open the Web App
        """
        return await self._client.call_method('getWebAppLinkUrl', {'@type': 'getWebAppLinkUrl', 'chat_id': chat_id, 'bot_user_id': bot_user_id, 'web_app_short_name': web_app_short_name, 'start_parameter': start_parameter, 'allow_write_access': allow_write_access, 'parameters': parameters})

    async def get_main_web_app(self, chat_id: int = None, bot_user_id: int = None, start_parameter: str = None, parameters: webAppOpenParameters = None) -> MainWebApp:
        """
        description Returns information needed to open the main Web App of a bot
        chat_id Identifier of the chat in which the Web App is opened; pass 0 if none
        bot_user_id Identifier of the target bot. If the bot is restricted for the current user, then show an error instead of calling the method
        start_parameter Start parameter from internalLinkTypeMainWebApp
        parameters Parameters to use to open the Web App
        """
        return await self._client.call_method('getMainWebApp', {'@type': 'getMainWebApp', 'chat_id': chat_id, 'bot_user_id': bot_user_id, 'start_parameter': start_parameter, 'parameters': parameters})

    async def get_web_app_url(self, bot_user_id: int = None, url: str = None, parameters: webAppOpenParameters = None) -> WebAppUrl:
        """
        description Returns an HTTPS URL of a Web App to open from the side menu, a keyboardButtonTypeWebApp button, or an inlineQueryResultsButtonTypeWebApp button
        bot_user_id Identifier of the target bot. If the bot is restricted for the current user, then show an error instead of calling the method
        url The URL from a keyboardButtonTypeWebApp button, inlineQueryResultsButtonTypeWebApp button, or an empty string when the bot is opened from the side menu
        parameters Parameters to use to open the Web App
        """
        return await self._client.call_method('getWebAppUrl', {'@type': 'getWebAppUrl', 'bot_user_id': bot_user_id, 'url': url, 'parameters': parameters})

    async def send_web_app_data(self, bot_user_id: int = None, button_text: str = None, data: str = None) -> Ok:
        """
        description Sends data received from a keyboardButtonTypeWebApp Web App to a bot
        bot_user_id Identifier of the target bot
        button_text Text of the keyboardButtonTypeWebApp button, which opened the Web App
        data The data
        """
        return await self._client.call_method('sendWebAppData', {'@type': 'sendWebAppData', 'bot_user_id': bot_user_id, 'button_text': button_text, 'data': data})

    async def open_web_app(self, chat_id: int = None, bot_user_id: int = None, url: str = None, topic_id: MessageTopic = None, reply_to: InputMessageReplyTo = None, parameters: webAppOpenParameters = None) -> WebAppInfo:
        """
        description Informs TDLib that a Web App is being opened from the attachment menu, a botMenuButton button, an internalLinkTypeAttachmentMenuBot link, or an inlineKeyboardButtonTypeWebApp button.
        chat_id Identifier of the chat in which the Web App is opened. The Web App can't be opened in secret chats
        bot_user_id Identifier of the bot, providing the Web App. If the bot is restricted for the current user, then show an error instead of calling the method
        url The URL from an inlineKeyboardButtonTypeWebApp button, a botMenuButton button, an internalLinkTypeAttachmentMenuBot link, or an empty string otherwise
        topic_id Topic in which the message will be sent; pass null if none
        reply_to Information about the message or story to be replied in the message sent by the Web App; pass null if none
        parameters Parameters to use to open the Web App
        """
        return await self._client.call_method('openWebApp', {'@type': 'openWebApp', 'chat_id': chat_id, 'bot_user_id': bot_user_id, 'url': url, 'topic_id': topic_id, 'reply_to': reply_to, 'parameters': parameters})

    async def close_web_app(self, web_app_launch_id: int = None) -> Ok:
        """
        description Informs TDLib that a previously opened Web App was closed @web_app_launch_id Identifier of Web App launch, received from openWebApp
        """
        return await self._client.call_method('closeWebApp', {'@type': 'closeWebApp', 'web_app_launch_id': web_app_launch_id})

    async def answer_web_app_query(self, web_app_query_id: str = None, result: InputInlineQueryResult = None) -> InlineMessageId:
        """
        description Sets the result of interaction with a Web App and sends corresponding message on behalf of the user to the chat from which the query originated; for bots only
        web_app_query_id Identifier of the Web App query
        result The result of the query
        """
        return await self._client.call_method('answerWebAppQuery', {'@type': 'answerWebAppQuery', 'web_app_query_id': web_app_query_id, 'result': result})

    async def check_web_app_file_download(self, bot_user_id: int = None, file_name: str = None, url: str = None) -> Ok:
        """
        description Checks whether a file can be downloaded and saved locally by Web App request
        bot_user_id Identifier of the bot, providing the Web App
        file_name Name of the file
        url URL of the file
        """
        return await self._client.call_method('checkWebAppFileDownload', {'@type': 'checkWebAppFileDownload', 'bot_user_id': bot_user_id, 'file_name': file_name, 'url': url})

    async def answer_chat_join_request_query(self, query_id: int = None, result: ChatJoinRequestResult = None, url: str = None) -> Ok:
        """
        description Sets the result of a chat join query; for bots only
        query_id Identifier of the query
        result The result
        url URL of the Web App to open
        """
        return await self._client.call_method('answerChatJoinRequestQuery', {'@type': 'answerChatJoinRequestQuery', 'query_id': query_id, 'result': result, 'url': url})

    async def get_callback_query_answer(self, chat_id: int = None, message_id: int = None, payload: CallbackQueryPayload = None) -> CallbackQueryAnswer:
        """
        description Sends a callback query to a bot and returns an answer. Returns an error with code 502 if the bot fails to answer the query before the query timeout expires
        chat_id Identifier of the chat with the message
        message_id Identifier of the message from which the query originated. The message must not be scheduled
        payload Query payload
        """
        return await self._client.call_method('getCallbackQueryAnswer', {'@type': 'getCallbackQueryAnswer', 'chat_id': chat_id, 'message_id': message_id, 'payload': payload})

    async def answer_callback_query(self, callback_query_id: int = None, text: str = None, show_alert: bool = None, url: str = None, cache_time: int = None) -> Ok:
        """
        description Sets the result of a callback query; for bots only
        callback_query_id Identifier of the callback query
        text Text of the answer
        show_alert Pass true to show an alert to the user instead of a toast notification
        url URL to be opened
        cache_time Time during which the result of the query can be cached, in seconds
        """
        return await self._client.call_method('answerCallbackQuery', {'@type': 'answerCallbackQuery', 'callback_query_id': callback_query_id, 'text': text, 'show_alert': show_alert, 'url': url, 'cache_time': cache_time})

    async def answer_shipping_query(self, shipping_query_id: int = None, shipping_options: List[shippingOption] = None, error_message: str = None) -> Ok:
        """
        description Sets the result of a shipping query; for bots only @shipping_query_id Identifier of the shipping query @shipping_options Available shipping options @error_message An error message, empty on success
        """
        return await self._client.call_method('answerShippingQuery', {'@type': 'answerShippingQuery', 'shipping_query_id': shipping_query_id, 'shipping_options': shipping_options, 'error_message': error_message})

    async def answer_pre_checkout_query(self, pre_checkout_query_id: int = None, error_message: str = None) -> Ok:
        """
        description Sets the result of a pre-checkout query; for bots only @pre_checkout_query_id Identifier of the pre-checkout query @error_message An error message, empty on success
        """
        return await self._client.call_method('answerPreCheckoutQuery', {'@type': 'answerPreCheckoutQuery', 'pre_checkout_query_id': pre_checkout_query_id, 'error_message': error_message})

    async def set_game_score(self, chat_id: int = None, message_id: int = None, edit_message: bool = None, user_id: int = None, score: int = None, force: bool = None) -> Message:
        """
        description Updates the game score of the specified user in the game; for bots only
        chat_id The chat to which the message with the game belongs
        message_id Identifier of the message
        edit_message Pass true to edit the game message to include the current scoreboard
        user_id User identifier
        score The new score
        force Pass true to update the score even if it decreases. If the score is 0, the user will be deleted from the high score table
        """
        return await self._client.call_method('setGameScore', {'@type': 'setGameScore', 'chat_id': chat_id, 'message_id': message_id, 'edit_message': edit_message, 'user_id': user_id, 'score': score, 'force': force})

    async def set_inline_game_score(self, inline_message_id: str = None, edit_message: bool = None, user_id: int = None, score: int = None, force: bool = None) -> Ok:
        """
        description Updates the game score of the specified user in a game; for bots only
        inline_message_id Inline message identifier
        edit_message Pass true to edit the game message to include the current scoreboard
        user_id User identifier
        score The new score
        force Pass true to update the score even if it decreases. If the score is 0, the user will be deleted from the high score table
        """
        return await self._client.call_method('setInlineGameScore', {'@type': 'setInlineGameScore', 'inline_message_id': inline_message_id, 'edit_message': edit_message, 'user_id': user_id, 'score': score, 'force': force})

    async def get_game_high_scores(self, chat_id: int = None, message_id: int = None, user_id: int = None) -> GameHighScores:
        """
        description Returns the high scores for a game and some part of the high score table in the range of the specified user; for bots only @chat_id The chat that contains the message with the game @message_id Identifier of the message @user_id User identifier
        """
        return await self._client.call_method('getGameHighScores', {'@type': 'getGameHighScores', 'chat_id': chat_id, 'message_id': message_id, 'user_id': user_id})

    async def get_inline_game_high_scores(self, inline_message_id: str = None, user_id: int = None) -> GameHighScores:
        """
        description Returns game high scores and some part of the high score table in the range of the specified user; for bots only @inline_message_id Inline message identifier @user_id User identifier
        """
        return await self._client.call_method('getInlineGameHighScores', {'@type': 'getInlineGameHighScores', 'inline_message_id': inline_message_id, 'user_id': user_id})

    async def delete_chat_reply_markup(self, chat_id: int = None, message_id: int = None) -> Ok:
        """
        description Deletes the default reply markup from a chat. Must be called after a one-time keyboard or a replyMarkupForceReply reply markup has been used or dismissed
        chat_id Chat identifier
        message_id The message identifier of the used keyboard
        """
        return await self._client.call_method('deleteChatReplyMarkup', {'@type': 'deleteChatReplyMarkup', 'chat_id': chat_id, 'message_id': message_id})

    async def send_chat_action(self, chat_id: int = None, topic_id: MessageTopic = None, business_connection_id: str = None, action: ChatAction = None) -> Ok:
        """
        description Sends a notification about user activity in a chat
        chat_id Chat identifier
        topic_id Identifier of the topic in which the action is performed; pass null if none
        business_connection_id Unique identifier of business connection on behalf of which to send the request; for bots only
        action The action description; pass null to cancel the currently active action
        """
        return await self._client.call_method('sendChatAction', {'@type': 'sendChatAction', 'chat_id': chat_id, 'topic_id': topic_id, 'business_connection_id': business_connection_id, 'action': action})

    async def send_text_message_draft(self, chat_id: int = None, forum_topic_id: int = None, draft_id: int = None, text: formattedText = None) -> Ok:
        """
        description Sends a draft for a being generated text message; for bots only
        chat_id Chat identifier
        forum_topic_id The forum topic identifier in which the message will be sent; pass 0 if none
        draft_id Unique identifier of the draft
        text Draft text of the message; pass null to show a "Thinking..." placeholder
        """
        return await self._client.call_method('sendTextMessageDraft', {'@type': 'sendTextMessageDraft', 'chat_id': chat_id, 'forum_topic_id': forum_topic_id, 'draft_id': draft_id, 'text': text})

    async def send_rich_message_draft(self, chat_id: int = None, forum_topic_id: int = None, draft_id: int = None, message: inputRichMessage = None) -> Ok:
        """
        description Sends a draft for a being generated rich message; for bots only
        chat_id Chat identifier
        forum_topic_id The forum topic identifier in which the message will be sent; pass 0 if none
        draft_id Unique identifier of the draft
        message Draft of the message
        """
        return await self._client.call_method('sendRichMessageDraft', {'@type': 'sendRichMessageDraft', 'chat_id': chat_id, 'forum_topic_id': forum_topic_id, 'draft_id': draft_id, 'message': message})

    async def open_chat(self, chat_id: int = None) -> Ok:
        """
        description Informs TDLib that the chat is opened by the user. Many useful activities depend on the chat being opened or closed (e.g., in supergroups and channels all updates are received only for opened chats) @chat_id Chat identifier
        """
        return await self._client.call_method('openChat', {'@type': 'openChat', 'chat_id': chat_id})

    async def close_chat(self, chat_id: int = None) -> Ok:
        """
        description Informs TDLib that the chat is closed by the user. Many useful activities depend on the chat being opened or closed @chat_id Chat identifier
        """
        return await self._client.call_method('closeChat', {'@type': 'closeChat', 'chat_id': chat_id})

    async def view_messages(self, chat_id: int = None, message_ids: List[int] = None, source: MessageSource = None, force_read: bool = None) -> Ok:
        """
        description Informs TDLib that messages are being viewed by the user. Sponsored messages must be marked as viewed only when the entire text of the message is shown on the screen (excluding the button).
        chat_id Chat identifier
        message_ids The identifiers of the messages being viewed
        source Source of the message view; pass null to guess the source based on chat open state
        force_read Pass true to mark as read the specified messages even if the chat is closed
        """
        return await self._client.call_method('viewMessages', {'@type': 'viewMessages', 'chat_id': chat_id, 'message_ids': message_ids, 'source': source, 'force_read': force_read})

    async def open_message_content(self, chat_id: int = None, message_id: int = None) -> Ok:
        """
        description Informs TDLib that the message content has been opened (e.g., the user has opened a photo, video, document, location or venue, or has listened to an audio file or voice note message).
        chat_id Chat identifier of the message
        message_id Identifier of the message with the opened content
        """
        return await self._client.call_method('openMessageContent', {'@type': 'openMessageContent', 'chat_id': chat_id, 'message_id': message_id})

    async def click_animated_emoji_message(self, chat_id: int = None, message_id: int = None) -> Sticker:
        """
        description Informs TDLib that a message with an animated emoji was clicked by the user. Returns a big animated sticker to be played or a 404 error if usual animation needs to be played @chat_id Chat identifier of the message @message_id Identifier of the clicked message
        """
        return await self._client.call_method('clickAnimatedEmojiMessage', {'@type': 'clickAnimatedEmojiMessage', 'chat_id': chat_id, 'message_id': message_id})

    async def listen_to_audio(self, audio_file_id: int = None, duration: int = None) -> Ok:
        """
        description Informs TDLib that an audio was listened by the user
        audio_file_id Identifier of the file with an audio
        duration Duration of the listening to the audio, in seconds
        """
        return await self._client.call_method('listenToAudio', {'@type': 'listenToAudio', 'audio_file_id': audio_file_id, 'duration': duration})

    async def send_message_view_metrics(self, chat_id: int = None, message_id: int = None, time_in_view_ms: int = None, active_time_in_view_ms: int = None, height_to_viewport_ratio_per_mille: int = None, seen_range_ratio_per_mille: int = None) -> Ok:
        """
        description Informs TDLib about details of a message view by the user from a chat, a message thread or a forum topic history. The method must be called if
        chat_id Chat identifier
        message_id The identifier of the message being viewed
        time_in_view_ms The amount of time the message was seen by at least 1 pixel; in milliseconds
        active_time_in_view_ms The amount of time the message was seen by at least 1 pixel within 15 seconds after any action from the user; in milliseconds
        height_to_viewport_ratio_per_mille The ratio of the post height to the viewport height in 1/1000 fractions
        seen_range_ratio_per_mille The ratio of the viewed post height to the full post height in 1/1000 fractions; 0-1000
        """
        return await self._client.call_method('sendMessageViewMetrics', {'@type': 'sendMessageViewMetrics', 'chat_id': chat_id, 'message_id': message_id, 'time_in_view_ms': time_in_view_ms, 'active_time_in_view_ms': active_time_in_view_ms, 'height_to_viewport_ratio_per_mille': height_to_viewport_ratio_per_mille, 'seen_range_ratio_per_mille': seen_range_ratio_per_mille})

    async def get_internal_link(self, type: InternalLinkType = None, is_http: bool = None) -> HttpUrl:
        """
        description Returns an HTTPS or a tg: link with the given type. Can be called before authorization @type Expected type of the link @is_http Pass true to create an HTTPS link (only available for some link types); pass false to create a tg: link
        """
        return await self._client.call_method('getInternalLink', {'@type': 'getInternalLink', 'type': type, 'is_http': is_http})

    async def get_internal_link_type(self, link: str = None) -> InternalLinkType:
        """
        description Returns information about the type of internal link. Returns a 404 error if the link is not internal. Can be called before authorization @link The link
        """
        return await self._client.call_method('getInternalLinkType', {'@type': 'getInternalLinkType', 'link': link})

    async def get_external_link_info(self, link: str = None) -> LoginUrlInfo:
        """
        description Returns information about an action to be done when the current user clicks an external link. Don't use this method for links from secret chats
        link The link
        """
        return await self._client.call_method('getExternalLinkInfo', {'@type': 'getExternalLinkInfo', 'link': link})

    async def get_external_link(self, link: str = None, allow_write_access: bool = None) -> HttpUrl:
        """
        description Returns an HTTP URL which can be used to automatically authorize the current user on a website after clicking an HTTP link.
        link The HTTP link
        allow_write_access Pass true if the current user allowed the bot that was returned in getExternalLinkInfo, to send them messages
        """
        return await self._client.call_method('getExternalLink', {'@type': 'getExternalLink', 'link': link, 'allow_write_access': allow_write_access})

    async def get_link_web_browser_type(self, link: str = None) -> WebBrowserType:
        """
        description Returns a type of the web browser which must be used to open the link
        link The HTTP link
        """
        return await self._client.call_method('getLinkWebBrowserType', {'@type': 'getLinkWebBrowserType', 'link': link})

    async def get_oauth_link_info(self, url: str = None, in_app_origin: str = None) -> OauthLinkInfo:
        """
        description Returns information about an OAuth deep link. Use checkOauthRequestMatchCode, acceptOauthRequest or declineOauthRequest to process the link
        url URL of the link
        in_app_origin Origin of the OAuth request if the request was received from the in-app browser; pass an empty string otherwise
        """
        return await self._client.call_method('getOauthLinkInfo', {'@type': 'getOauthLinkInfo', 'url': url, 'in_app_origin': in_app_origin})

    async def check_oauth_request_match_code(self, url: str = None, match_code: str = None) -> Ok:
        """
        description Checks a match-code for an OAuth authorization request. If fails, then the authorization request has failed. Otherwise,
        url URL of the OAuth deep link
        match_code The matching code chosen by the user
        """
        return await self._client.call_method('checkOauthRequestMatchCode', {'@type': 'checkOauthRequestMatchCode', 'url': url, 'match_code': match_code})

    async def accept_oauth_request(self, url: str = None, match_code: str = None, allow_write_access: bool = None, allow_phone_number_access: bool = None) -> HttpUrl:
        """
        description Accepts an OAuth authorization request. Returns an HTTP URL to open after successful authorization.
        url URL of the OAuth deep link
        match_code The matching code chosen by the user
        allow_write_access Pass true if the current user allowed the bot that was returned in getOauthLinkInfo, to send them messages
        allow_phone_number_access Pass true if the current user allowed the bot that was returned in getOauthLinkInfo, to access their phone number
        """
        return await self._client.call_method('acceptOauthRequest', {'@type': 'acceptOauthRequest', 'url': url, 'match_code': match_code, 'allow_write_access': allow_write_access, 'allow_phone_number_access': allow_phone_number_access})

    async def decline_oauth_request(self, url: str = None) -> Ok:
        """
        description Declines an OAuth authorization request
        url URL of the OAuth deep link
        """
        return await self._client.call_method('declineOauthRequest', {'@type': 'declineOauthRequest', 'url': url})

    async def read_all_chat_mentions(self, chat_id: int = None) -> Ok:
        """
        description Marks all mentions in a chat as read @chat_id Chat identifier
        """
        return await self._client.call_method('readAllChatMentions', {'@type': 'readAllChatMentions', 'chat_id': chat_id})

    async def read_all_chat_reactions(self, chat_id: int = None) -> Ok:
        """
        description Marks all reactions in a chat as read @chat_id Chat identifier
        """
        return await self._client.call_method('readAllChatReactions', {'@type': 'readAllChatReactions', 'chat_id': chat_id})

    async def read_all_chat_poll_votes(self, chat_id: int = None) -> Ok:
        """
        description Marks all poll votes in a chat as read @chat_id Chat identifier
        """
        return await self._client.call_method('readAllChatPollVotes', {'@type': 'readAllChatPollVotes', 'chat_id': chat_id})

    async def create_private_chat(self, user_id: int = None, force: bool = None) -> Chat:
        """
        description Returns an existing chat corresponding to a given user @user_id User identifier @force Pass true to create the chat without a network request. In this case all information about the chat except its type, title and photo can be incorrect
        """
        return await self._client.call_method('createPrivateChat', {'@type': 'createPrivateChat', 'user_id': user_id, 'force': force})

    async def create_basic_group_chat(self, basic_group_id: int = None, force: bool = None) -> Chat:
        """
        description Returns an existing chat corresponding to a known basic group @basic_group_id Basic group identifier @force Pass true to create the chat without a network request. In this case all information about the chat except its type, title and photo can be incorrect
        """
        return await self._client.call_method('createBasicGroupChat', {'@type': 'createBasicGroupChat', 'basic_group_id': basic_group_id, 'force': force})

    async def create_supergroup_chat(self, supergroup_id: int = None, force: bool = None) -> Chat:
        """
        description Returns an existing chat corresponding to a known supergroup or channel @supergroup_id Supergroup or channel identifier @force Pass true to create the chat without a network request. In this case all information about the chat except its type, title and photo can be incorrect
        """
        return await self._client.call_method('createSupergroupChat', {'@type': 'createSupergroupChat', 'supergroup_id': supergroup_id, 'force': force})

    async def create_secret_chat(self, secret_chat_id: int = None) -> Chat:
        """
        description Returns an existing chat corresponding to a known secret chat @secret_chat_id Secret chat identifier
        """
        return await self._client.call_method('createSecretChat', {'@type': 'createSecretChat', 'secret_chat_id': secret_chat_id})

    async def create_new_basic_group_chat(self, user_ids: List[int] = None, title: str = None, message_auto_delete_time: int = None) -> CreatedBasicGroupChat:
        """
        description Creates a new basic group and sends a corresponding messageBasicGroupChatCreate. Returns information about the newly created chat
        user_ids Identifiers of users to be added to the basic group; may be empty to create a basic group without other members
        title Title of the new basic group; 1-128 characters
        message_auto_delete_time Message auto-delete time value, in seconds; must be from 0 up to 365 * 86400 and be divisible by 86400. If 0, then messages aren't deleted automatically
        """
        return await self._client.call_method('createNewBasicGroupChat', {'@type': 'createNewBasicGroupChat', 'user_ids': user_ids, 'title': title, 'message_auto_delete_time': message_auto_delete_time})

    async def create_new_supergroup_chat(self, title: str = None, is_forum: bool = None, is_channel: bool = None, description: str = None, location: chatLocation = None, message_auto_delete_time: int = None, for_import: bool = None) -> Chat:
        """
        description Creates a new supergroup or channel and sends a corresponding messageSupergroupChatCreate. Returns the newly created chat
        title Title of the new chat; 1-128 characters
        is_forum Pass true to create a forum supergroup chat
        is_channel Pass true to create a channel chat; ignored if a forum is created
        param_description Chat description; 0-255 characters
        location Chat location if a location-based supergroup is being created; pass null to create an ordinary supergroup chat
        message_auto_delete_time Message auto-delete time value, in seconds; must be from 0 up to 365 * 86400 and be divisible by 86400. If 0, then messages aren't deleted automatically
        for_import Pass true to create a supergroup for importing messages using importMessages
        """
        return await self._client.call_method('createNewSupergroupChat', {'@type': 'createNewSupergroupChat', 'title': title, 'is_forum': is_forum, 'is_channel': is_channel, 'description': description, 'location': location, 'message_auto_delete_time': message_auto_delete_time, 'for_import': for_import})

    async def create_new_secret_chat(self, user_id: int = None) -> Chat:
        """
        description Creates a new secret chat. Returns the newly created chat @user_id Identifier of the target user
        """
        return await self._client.call_method('createNewSecretChat', {'@type': 'createNewSecretChat', 'user_id': user_id})

    async def upgrade_basic_group_chat_to_supergroup_chat(self, chat_id: int = None) -> Chat:
        """
        description Creates a new supergroup from an existing basic group and sends a corresponding messageChatUpgradeTo and messageChatUpgradeFrom; requires owner privileges. Deactivates the original basic group @chat_id Identifier of the chat to upgrade
        """
        return await self._client.call_method('upgradeBasicGroupChatToSupergroupChat', {'@type': 'upgradeBasicGroupChatToSupergroupChat', 'chat_id': chat_id})

    async def get_chat_lists_to_add_chat(self, chat_id: int = None) -> ChatLists:
        """
        description Returns chat lists to which the chat can be added. This is an offline method @chat_id Chat identifier
        """
        return await self._client.call_method('getChatListsToAddChat', {'@type': 'getChatListsToAddChat', 'chat_id': chat_id})

    async def add_chat_to_list(self, chat_id: int = None, chat_list: ChatList = None) -> Ok:
        """
        description Adds a chat to a chat list. A chat can't be simultaneously in Main and Archive chat lists, so it is automatically removed from another one if needed
        chat_id Chat identifier
        chat_list The chat list. Use getChatListsToAddChat to get suitable chat lists
        """
        return await self._client.call_method('addChatToList', {'@type': 'addChatToList', 'chat_id': chat_id, 'chat_list': chat_list})

    async def get_chat_folder(self, chat_folder_id: int = None) -> ChatFolder:
        """
        description Returns information about a chat folder by its identifier @chat_folder_id Chat folder identifier
        """
        return await self._client.call_method('getChatFolder', {'@type': 'getChatFolder', 'chat_folder_id': chat_folder_id})

    async def create_chat_folder(self, folder: chatFolder = None) -> ChatFolderInfo:
        """
        description Creates new chat folder. Returns information about the created chat folder. There can be up to getOption("chat_folder_count_max") chat folders, but the limit can be increased with Telegram Premium @folder The new chat folder
        """
        return await self._client.call_method('createChatFolder', {'@type': 'createChatFolder', 'folder': folder})

    async def edit_chat_folder(self, chat_folder_id: int = None, folder: chatFolder = None) -> ChatFolderInfo:
        """
        description Edits existing chat folder. Returns information about the edited chat folder @chat_folder_id Chat folder identifier @folder The edited chat folder
        """
        return await self._client.call_method('editChatFolder', {'@type': 'editChatFolder', 'chat_folder_id': chat_folder_id, 'folder': folder})

    async def delete_chat_folder(self, chat_folder_id: int = None, leave_chat_ids: List[int] = None) -> Ok:
        """
        description Deletes existing chat folder @chat_folder_id Chat folder identifier @leave_chat_ids Identifiers of the chats to leave. The chats must be pinned or always included in the folder
        """
        return await self._client.call_method('deleteChatFolder', {'@type': 'deleteChatFolder', 'chat_folder_id': chat_folder_id, 'leave_chat_ids': leave_chat_ids})

    async def get_chat_folder_chats_to_leave(self, chat_folder_id: int = None) -> Chats:
        """
        description Returns identifiers of pinned or always included chats from a chat folder, which are suggested to be left when the chat folder is deleted @chat_folder_id Chat folder identifier
        """
        return await self._client.call_method('getChatFolderChatsToLeave', {'@type': 'getChatFolderChatsToLeave', 'chat_folder_id': chat_folder_id})

    async def get_chat_folder_chat_count(self, folder: chatFolder = None) -> Count:
        """
        description Returns approximate number of chats in a being created chat folder. Main and archive chat lists must be fully preloaded for this function to work correctly @folder The new chat folder
        """
        return await self._client.call_method('getChatFolderChatCount', {'@type': 'getChatFolderChatCount', 'folder': folder})

    async def reorder_chat_folders(self, chat_folder_ids: List[int] = None, main_chat_list_position: int = None) -> Ok:
        """
        description Changes the order of chat folders @chat_folder_ids Identifiers of chat folders in the new correct order @main_chat_list_position Position of the main chat list among chat folders, 0-based. Can be non-zero only for Premium users
        """
        return await self._client.call_method('reorderChatFolders', {'@type': 'reorderChatFolders', 'chat_folder_ids': chat_folder_ids, 'main_chat_list_position': main_chat_list_position})

    async def toggle_chat_folder_tags(self, are_tags_enabled: bool = None) -> Ok:
        """
        description Toggles whether chat folder tags are enabled @are_tags_enabled Pass true to enable folder tags; pass false to disable them
        """
        return await self._client.call_method('toggleChatFolderTags', {'@type': 'toggleChatFolderTags', 'are_tags_enabled': are_tags_enabled})

    async def get_recommended_chat_folders(self) -> RecommendedChatFolders:
        """
        description Returns recommended chat folders for the current user
        """
        return await self._client.call_method('getRecommendedChatFolders', {'@type': 'getRecommendedChatFolders'})

    async def get_chat_folder_default_icon_name(self, folder: chatFolder = None) -> ChatFolderIcon:
        """
        description Returns default icon name for a folder. Can be called synchronously @folder Chat folder
        """
        return await self._client.call_method('getChatFolderDefaultIconName', {'@type': 'getChatFolderDefaultIconName', 'folder': folder})

    async def get_chats_for_chat_folder_invite_link(self, chat_folder_id: int = None) -> Chats:
        """
        description Returns identifiers of chats from a chat folder, suitable for adding to a chat folder invite link @chat_folder_id Chat folder identifier
        """
        return await self._client.call_method('getChatsForChatFolderInviteLink', {'@type': 'getChatsForChatFolderInviteLink', 'chat_folder_id': chat_folder_id})

    async def create_chat_folder_invite_link(self, chat_folder_id: int = None, name: str = None, chat_ids: List[int] = None) -> ChatFolderInviteLink:
        """
        description Creates a new invite link for a chat folder. A link can be created for a chat folder if it has only pinned and included chats
        chat_folder_id Chat folder identifier
        name Name of the link; 0-32 characters
        chat_ids Identifiers of chats to be accessible by the invite link. Use getChatsForChatFolderInviteLink to get suitable chats. Basic groups will be automatically converted to supergroups before link creation
        """
        return await self._client.call_method('createChatFolderInviteLink', {'@type': 'createChatFolderInviteLink', 'chat_folder_id': chat_folder_id, 'name': name, 'chat_ids': chat_ids})

    async def get_chat_folder_invite_links(self, chat_folder_id: int = None) -> ChatFolderInviteLinks:
        """
        description Returns invite links created by the current user for a shareable chat folder @chat_folder_id Chat folder identifier
        """
        return await self._client.call_method('getChatFolderInviteLinks', {'@type': 'getChatFolderInviteLinks', 'chat_folder_id': chat_folder_id})

    async def edit_chat_folder_invite_link(self, chat_folder_id: int = None, invite_link: str = None, name: str = None, chat_ids: List[int] = None) -> ChatFolderInviteLink:
        """
        description Edits an invite link for a chat folder
        chat_folder_id Chat folder identifier
        invite_link Invite link to be edited
        name New name of the link; 0-32 characters
        chat_ids New identifiers of chats to be accessible by the invite link. Use getChatsForChatFolderInviteLink to get suitable chats. Basic groups will be automatically converted to supergroups before link editing
        """
        return await self._client.call_method('editChatFolderInviteLink', {'@type': 'editChatFolderInviteLink', 'chat_folder_id': chat_folder_id, 'invite_link': invite_link, 'name': name, 'chat_ids': chat_ids})

    async def delete_chat_folder_invite_link(self, chat_folder_id: int = None, invite_link: str = None) -> Ok:
        """
        description Deletes an invite link for a chat folder
        chat_folder_id Chat folder identifier
        invite_link Invite link to be deleted
        """
        return await self._client.call_method('deleteChatFolderInviteLink', {'@type': 'deleteChatFolderInviteLink', 'chat_folder_id': chat_folder_id, 'invite_link': invite_link})

    async def check_chat_folder_invite_link(self, invite_link: str = None) -> ChatFolderInviteLinkInfo:
        """
        description Checks the validity of an invite link for a chat folder and returns information about the corresponding chat folder @invite_link Invite link to be checked
        """
        return await self._client.call_method('checkChatFolderInviteLink', {'@type': 'checkChatFolderInviteLink', 'invite_link': invite_link})

    async def add_chat_folder_by_invite_link(self, invite_link: str = None, chat_ids: List[int] = None) -> Ok:
        """
        description Adds a chat folder by an invite link @invite_link Invite link for the chat folder @chat_ids Identifiers of the chats added to the chat folder. The chats are automatically joined if they aren't joined yet
        """
        return await self._client.call_method('addChatFolderByInviteLink', {'@type': 'addChatFolderByInviteLink', 'invite_link': invite_link, 'chat_ids': chat_ids})

    async def get_chat_folder_new_chats(self, chat_folder_id: int = None) -> Chats:
        """
        description Returns new chats added to a shareable chat folder by its owner. The method must be called at most once in getOption("chat_folder_new_chats_update_period") for the given chat folder @chat_folder_id Chat folder identifier
        """
        return await self._client.call_method('getChatFolderNewChats', {'@type': 'getChatFolderNewChats', 'chat_folder_id': chat_folder_id})

    async def process_chat_folder_new_chats(self, chat_folder_id: int = None, added_chat_ids: List[int] = None) -> Ok:
        """
        description Process new chats added to a shareable chat folder by its owner @chat_folder_id Chat folder identifier @added_chat_ids Identifiers of the new chats, which are added to the chat folder. The chats are automatically joined if they aren't joined yet
        """
        return await self._client.call_method('processChatFolderNewChats', {'@type': 'processChatFolderNewChats', 'chat_folder_id': chat_folder_id, 'added_chat_ids': added_chat_ids})

    async def get_archive_chat_list_settings(self) -> ArchiveChatListSettings:
        """
        description Returns settings for automatic moving of chats to and from the Archive chat lists
        """
        return await self._client.call_method('getArchiveChatListSettings', {'@type': 'getArchiveChatListSettings'})

    async def set_archive_chat_list_settings(self, settings: archiveChatListSettings = None) -> Ok:
        """
        description Changes settings for automatic moving of chats to and from the Archive chat lists @settings New settings
        """
        return await self._client.call_method('setArchiveChatListSettings', {'@type': 'setArchiveChatListSettings', 'settings': settings})

    async def set_chat_title(self, chat_id: int = None, title: str = None) -> Ok:
        """
        description Changes the chat title. Supported only for basic groups, supergroups and channels. Requires can_change_info member right
        chat_id Chat identifier
        title New title of the chat; 1-128 characters
        """
        return await self._client.call_method('setChatTitle', {'@type': 'setChatTitle', 'chat_id': chat_id, 'title': title})

    async def set_chat_photo(self, chat_id: int = None, photo: InputChatPhoto = None) -> Ok:
        """
        description Changes the photo of a chat. Supported only for basic groups, supergroups and channels. Requires can_change_info member right
        chat_id Chat identifier
        photo New chat photo; pass null to delete the chat photo
        """
        return await self._client.call_method('setChatPhoto', {'@type': 'setChatPhoto', 'chat_id': chat_id, 'photo': photo})

    async def set_chat_accent_color(self, chat_id: int = None, accent_color_id: int = None, background_custom_emoji_id: int = None) -> Ok:
        """
        description Changes accent color and background custom emoji of a channel chat. Requires can_change_info administrator right
        chat_id Chat identifier
        accent_color_id Identifier of the accent color to use. The chat must have at least accentColor.min_channel_chat_boost_level boost level to pass the corresponding color
        background_custom_emoji_id Identifier of a custom emoji to be shown on the reply header and link preview background; 0 if none. Use chatBoostLevelFeatures.can_set_background_custom_emoji to check whether a custom emoji can be set
        """
        return await self._client.call_method('setChatAccentColor', {'@type': 'setChatAccentColor', 'chat_id': chat_id, 'accent_color_id': accent_color_id, 'background_custom_emoji_id': background_custom_emoji_id})

    async def set_chat_profile_accent_color(self, chat_id: int = None, profile_accent_color_id: int = None, profile_background_custom_emoji_id: int = None) -> Ok:
        """
        description Changes accent color and background custom emoji for profile of a supergroup or channel chat. Requires can_change_info administrator right
        chat_id Chat identifier
        profile_accent_color_id Identifier of the accent color to use for profile; pass -1 if none. The chat must have at least profileAccentColor.min_supergroup_chat_boost_level for supergroups
        profile_background_custom_emoji_id Identifier of a custom emoji to be shown on the chat's profile photo background; 0 if none. Use chatBoostLevelFeatures.can_set_profile_background_custom_emoji to check whether a custom emoji can be set
        """
        return await self._client.call_method('setChatProfileAccentColor', {'@type': 'setChatProfileAccentColor', 'chat_id': chat_id, 'profile_accent_color_id': profile_accent_color_id, 'profile_background_custom_emoji_id': profile_background_custom_emoji_id})

    async def set_chat_message_auto_delete_time(self, chat_id: int = None, message_auto_delete_time: int = None) -> Ok:
        """
        description Changes the message auto-delete or self-destruct (for secret chats) time in a chat. Requires change_info administrator right in basic groups, supergroups and channels.
        chat_id Chat identifier
        message_auto_delete_time New time value, in seconds; unless the chat is secret, it must be from 0 up to 365 * 86400 and be divisible by 86400. If 0, then messages aren't deleted automatically
        """
        return await self._client.call_method('setChatMessageAutoDeleteTime', {'@type': 'setChatMessageAutoDeleteTime', 'chat_id': chat_id, 'message_auto_delete_time': message_auto_delete_time})

    async def set_chat_emoji_status(self, chat_id: int = None, emoji_status: emojiStatus = None) -> Ok:
        """
        description Changes the emoji status of a chat. Use chatBoostLevelFeatures.can_set_emoji_status to check whether an emoji status can be set. Requires can_change_info administrator right
        chat_id Chat identifier
        emoji_status New emoji status; pass null to remove emoji status
        """
        return await self._client.call_method('setChatEmojiStatus', {'@type': 'setChatEmojiStatus', 'chat_id': chat_id, 'emoji_status': emoji_status})

    async def set_chat_permissions(self, chat_id: int = None, permissions: chatPermissions = None) -> Ok:
        """
        description Changes the chat members permissions. Supported only for basic groups and supergroups. Requires can_restrict_members administrator right
        chat_id Chat identifier
        permissions New non-administrator members permissions in the chat
        """
        return await self._client.call_method('setChatPermissions', {'@type': 'setChatPermissions', 'chat_id': chat_id, 'permissions': permissions})

    async def set_chat_background(self, chat_id: int = None, background: InputBackground = None, type: BackgroundType = None, dark_theme_dimming: int = None, only_for_self: bool = None) -> Ok:
        """
        description Sets the background in a specific chat. Supported only in private and secret chats with non-deleted users, and in chats with sufficient boost level and can_change_info administrator right
        chat_id Chat identifier
        background The input background to use; pass null to create a new filled or chat theme background
        type Background type; pass null to use default background type for the chosen background; backgroundTypeChatTheme isn't supported for private and secret chats.
        dark_theme_dimming Dimming of the background in dark themes, as a percentage; 0-100. Applied only to Wallpaper and Fill types of background
        only_for_self Pass true to set background only for self; pass false to set background for all chat users. Always false for backgrounds set in boosted chats. Background can be set for both users only by Telegram Premium users and if set background isn't of the type inputBackgroundPrevious
        """
        return await self._client.call_method('setChatBackground', {'@type': 'setChatBackground', 'chat_id': chat_id, 'background': background, 'type': type, 'dark_theme_dimming': dark_theme_dimming, 'only_for_self': only_for_self})

    async def delete_chat_background(self, chat_id: int = None, restore_previous: bool = None) -> Ok:
        """
        description Deletes background in a specific chat
        chat_id Chat identifier
        restore_previous Pass true to restore previously set background. Can be used only in private and secret chats with non-deleted users if userFullInfo.set_chat_background == true.
        """
        return await self._client.call_method('deleteChatBackground', {'@type': 'deleteChatBackground', 'chat_id': chat_id, 'restore_previous': restore_previous})

    async def get_gift_chat_themes(self, offset: str = None, limit: int = None) -> GiftChatThemes:
        """
        description Returns available to the current user gift chat themes
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of chat themes to return
        """
        return await self._client.call_method('getGiftChatThemes', {'@type': 'getGiftChatThemes', 'offset': offset, 'limit': limit})

    async def set_chat_theme(self, chat_id: int = None, theme: InputChatTheme = None) -> Ok:
        """
        description Changes the chat theme. Supported only in private and secret chats @chat_id Chat identifier @theme New chat theme; pass null to return the default theme
        """
        return await self._client.call_method('setChatTheme', {'@type': 'setChatTheme', 'chat_id': chat_id, 'theme': theme})

    async def set_chat_draft_message(self, chat_id: int = None, topic_id: MessageTopic = None, draft_message: draftMessage = None) -> Ok:
        """
        description Changes the draft message in a chat or a topic
        chat_id Chat identifier
        topic_id Topic in which the draft will be changed; pass null to change the draft for the chat itself
        draft_message New draft message; pass null to remove the draft. All files in draft message content must be of the type inputFileLocal. Media thumbnails and captions are ignored
        """
        return await self._client.call_method('setChatDraftMessage', {'@type': 'setChatDraftMessage', 'chat_id': chat_id, 'topic_id': topic_id, 'draft_message': draft_message})

    async def set_chat_notification_settings(self, chat_id: int = None, notification_settings: chatNotificationSettings = None) -> Ok:
        """
        description Changes the notification settings of a chat. Notification settings of a chat with the current user (Saved Messages) can't be changed
        chat_id Chat identifier
        notification_settings New notification settings for the chat. If the chat is muted for more than 366 days, it is considered to be muted forever
        """
        return await self._client.call_method('setChatNotificationSettings', {'@type': 'setChatNotificationSettings', 'chat_id': chat_id, 'notification_settings': notification_settings})

    async def toggle_chat_has_protected_content(self, chat_id: int = None, has_protected_content: bool = None) -> Ok:
        """
        description Changes the ability of users to save, forward, or copy chat content. Requires owner privileges in basic groups, supergroups and channels.
        chat_id Chat identifier
        has_protected_content New value of has_protected_content
        """
        return await self._client.call_method('toggleChatHasProtectedContent', {'@type': 'toggleChatHasProtectedContent', 'chat_id': chat_id, 'has_protected_content': has_protected_content})

    async def process_chat_has_protected_content_disable_request(self, chat_id: int = None, request_message_id: int = None, approve: bool = None) -> Ok:
        """
        description Processes request to disable has_protected_content in a chat
        chat_id Chat identifier
        request_message_id Identifier of the message with the request. The message must be incoming and has content of the type messageChatHasProtectedContentDisableRequested
        approve Pass true to approve the request; pass false to reject the request
        """
        return await self._client.call_method('processChatHasProtectedContentDisableRequest', {'@type': 'processChatHasProtectedContentDisableRequest', 'chat_id': chat_id, 'request_message_id': request_message_id, 'approve': approve})

    async def toggle_chat_view_as_topics(self, chat_id: int = None, view_as_topics: bool = None) -> Ok:
        """
        description Changes the view_as_topics setting of a forum chat or Saved Messages @chat_id Chat identifier @view_as_topics New value of view_as_topics
        """
        return await self._client.call_method('toggleChatViewAsTopics', {'@type': 'toggleChatViewAsTopics', 'chat_id': chat_id, 'view_as_topics': view_as_topics})

    async def toggle_chat_is_translatable(self, chat_id: int = None, is_translatable: bool = None) -> Ok:
        """
        description Changes the translatable state of a chat @chat_id Chat identifier @is_translatable New value of is_translatable
        """
        return await self._client.call_method('toggleChatIsTranslatable', {'@type': 'toggleChatIsTranslatable', 'chat_id': chat_id, 'is_translatable': is_translatable})

    async def toggle_chat_is_marked_as_unread(self, chat_id: int = None, is_marked_as_unread: bool = None) -> Ok:
        """
        description Changes the marked as unread state of a chat @chat_id Chat identifier @is_marked_as_unread New value of is_marked_as_unread
        """
        return await self._client.call_method('toggleChatIsMarkedAsUnread', {'@type': 'toggleChatIsMarkedAsUnread', 'chat_id': chat_id, 'is_marked_as_unread': is_marked_as_unread})

    async def toggle_chat_default_disable_notification(self, chat_id: int = None, default_disable_notification: bool = None) -> Ok:
        """
        description Changes the value of the default disable_notification parameter, used when a message is sent to a chat @chat_id Chat identifier @default_disable_notification New value of default_disable_notification
        """
        return await self._client.call_method('toggleChatDefaultDisableNotification', {'@type': 'toggleChatDefaultDisableNotification', 'chat_id': chat_id, 'default_disable_notification': default_disable_notification})

    async def set_chat_available_reactions(self, chat_id: int = None, available_reactions: ChatAvailableReactions = None) -> Ok:
        """
        description Changes reactions, available in a chat. Available for basic groups, supergroups, and channels. Requires can_change_info member right
        chat_id Identifier of the chat
        available_reactions Reactions available in the chat. All explicitly specified emoji reactions must be active. In channel chats up to the chat's boost level custom emoji reactions can be explicitly specified
        """
        return await self._client.call_method('setChatAvailableReactions', {'@type': 'setChatAvailableReactions', 'chat_id': chat_id, 'available_reactions': available_reactions})

    async def set_chat_client_data(self, chat_id: int = None, client_data: str = None) -> Ok:
        """
        description Changes application-specific data associated with a chat @chat_id Chat identifier @client_data New value of client_data
        """
        return await self._client.call_method('setChatClientData', {'@type': 'setChatClientData', 'chat_id': chat_id, 'client_data': client_data})

    async def set_chat_description(self, chat_id: int = None, description: str = None) -> Ok:
        """
        description Changes information about a chat. Available for basic groups, supergroups, and channels. Requires can_change_info member right @chat_id Identifier of the chat @param_description New chat description; 0-255 characters
        """
        return await self._client.call_method('setChatDescription', {'@type': 'setChatDescription', 'chat_id': chat_id, 'description': description})

    async def set_chat_discussion_group(self, chat_id: int = None, discussion_chat_id: int = None) -> Ok:
        """
        description Changes the discussion group of a channel chat; requires can_change_info administrator right in the channel if it is specified
        chat_id Identifier of the channel chat. Pass 0 to remove a link from the supergroup passed in the second argument to a linked channel chat (requires can_pin_messages member right in the supergroup)
        discussion_chat_id Identifier of a new channel's discussion group. Use 0 to remove the discussion group. Use the method getSuitableDiscussionChats to find all suitable groups.
        """
        return await self._client.call_method('setChatDiscussionGroup', {'@type': 'setChatDiscussionGroup', 'chat_id': chat_id, 'discussion_chat_id': discussion_chat_id})

    async def set_chat_direct_messages_group(self, chat_id: int = None, is_enabled: bool = None, paid_message_star_count: int = None) -> Ok:
        """
        description Changes direct messages group settings for a channel chat; requires owner privileges in the chat
        chat_id Identifier of the channel chat
        is_enabled Pass true if the direct messages group is enabled for the channel chat; pass false otherwise
        paid_message_star_count The new number of Telegram Stars that must be paid for each message that is sent to the direct messages chat unless the sender is an administrator of the channel chat; 0-getOption("paid_message_star_count_max").
        """
        return await self._client.call_method('setChatDirectMessagesGroup', {'@type': 'setChatDirectMessagesGroup', 'chat_id': chat_id, 'is_enabled': is_enabled, 'paid_message_star_count': paid_message_star_count})

    async def set_chat_location(self, chat_id: int = None, location: chatLocation = None) -> Ok:
        """
        description Changes the location of a chat. Available only for some location-based supergroups, use supergroupFullInfo.can_set_location to check whether the method is allowed to use @chat_id Chat identifier @location New location for the chat; must be valid and not null
        """
        return await self._client.call_method('setChatLocation', {'@type': 'setChatLocation', 'chat_id': chat_id, 'location': location})

    async def set_chat_slow_mode_delay(self, chat_id: int = None, slow_mode_delay: int = None) -> Ok:
        """
        description Changes the slow mode delay of a chat. Available only for supergroups; requires can_restrict_members administrator right @chat_id Chat identifier @slow_mode_delay New slow mode delay for the chat, in seconds; must be one of 0, 5, 10, 30, 60, 300, 900, 3600
        """
        return await self._client.call_method('setChatSlowModeDelay', {'@type': 'setChatSlowModeDelay', 'chat_id': chat_id, 'slow_mode_delay': slow_mode_delay})

    async def pin_chat_message(self, chat_id: int = None, message_id: int = None, disable_notification: bool = None, only_for_self: bool = None) -> Ok:
        """
        description Pins a message in a chat. A message can be pinned only if messageProperties.can_be_pinned
        chat_id Identifier of the chat
        message_id Identifier of the new pinned message
        disable_notification Pass true to disable notification about the pinned message. Notifications are always disabled in channels and private chats
        only_for_self Pass true to pin the message only for self; private chats only
        """
        return await self._client.call_method('pinChatMessage', {'@type': 'pinChatMessage', 'chat_id': chat_id, 'message_id': message_id, 'disable_notification': disable_notification, 'only_for_self': only_for_self})

    async def unpin_chat_message(self, chat_id: int = None, message_id: int = None) -> Ok:
        """
        description Removes a pinned message from a chat; requires can_pin_messages member right if the chat is a basic group or supergroup, or can_edit_messages administrator right if the chat is a channel @chat_id Identifier of the chat @message_id Identifier of the removed pinned message
        """
        return await self._client.call_method('unpinChatMessage', {'@type': 'unpinChatMessage', 'chat_id': chat_id, 'message_id': message_id})

    async def unpin_all_chat_messages(self, chat_id: int = None) -> Ok:
        """
        description Removes all pinned messages from a chat; requires can_pin_messages member right if the chat is a basic group or supergroup, or can_edit_messages administrator right if the chat is a channel @chat_id Identifier of the chat
        """
        return await self._client.call_method('unpinAllChatMessages', {'@type': 'unpinAllChatMessages', 'chat_id': chat_id})

    async def join_chat(self, chat_id: int = None) -> ChatJoinResult:
        """
        description Adds the current user as a new member to a chat. Private and secret chats can't be joined using this method @chat_id Chat identifier
        """
        return await self._client.call_method('joinChat', {'@type': 'joinChat', 'chat_id': chat_id})

    async def leave_chat(self, chat_id: int = None) -> Ok:
        """
        description Removes the current user from chat members. Private and secret chats can't be left using this method @chat_id Chat identifier
        """
        return await self._client.call_method('leaveChat', {'@type': 'leaveChat', 'chat_id': chat_id})

    async def add_chat_member(self, chat_id: int = None, user_id: int = None, forward_limit: int = None) -> FailedToAddMembers:
        """
        description Adds a new member to a chat; requires can_invite_users member right. Members can't be added to private or secret chats. Returns information about members that weren't added
        chat_id Chat identifier
        user_id Identifier of the user
        forward_limit The number of earlier messages from the chat to be forwarded to the new member; up to 100. Ignored for supergroups and channels, or if the added user is a bot
        """
        return await self._client.call_method('addChatMember', {'@type': 'addChatMember', 'chat_id': chat_id, 'user_id': user_id, 'forward_limit': forward_limit})

    async def add_chat_members(self, chat_id: int = None, user_ids: List[int] = None) -> FailedToAddMembers:
        """
        description Adds multiple new members to a chat; requires can_invite_users member right. Currently, this method is only available for supergroups and channels.
        chat_id Chat identifier
        user_ids Identifiers of the users to be added to the chat. The maximum number of added users is 20 for supergroups and 100 for channels
        """
        return await self._client.call_method('addChatMembers', {'@type': 'addChatMembers', 'chat_id': chat_id, 'user_ids': user_ids})

    async def set_chat_member_status(self, chat_id: int = None, member_id: MessageSender = None, status: ChatMemberStatus = None) -> Ok:
        """
        description Changes the status of a chat member; requires can_invite_users member right to add a chat member, can_promote_members administrator right to change administrator rights of the member,
        chat_id Chat identifier
        member_id Member identifier. Chats can be only banned and unbanned in supergroups and channels
        status The new status of the member in the chat
        """
        return await self._client.call_method('setChatMemberStatus', {'@type': 'setChatMemberStatus', 'chat_id': chat_id, 'member_id': member_id, 'status': status})

    async def set_chat_member_tag(self, chat_id: int = None, user_id: int = None, tag: str = None) -> Ok:
        """
        description Changes the tag or custom title of a chat member; requires can_manage_tags administrator right to change tag of other users; for basic groups and supergroups only
        chat_id Chat identifier
        user_id Identifier of the user, which tag is changed. Chats can't have member tags
        tag The new tag of the member in the chat; 0-16 characters without emoji
        """
        return await self._client.call_method('setChatMemberTag', {'@type': 'setChatMemberTag', 'chat_id': chat_id, 'user_id': user_id, 'tag': tag})

    async def ban_chat_member(self, chat_id: int = None, member_id: MessageSender = None, banned_until_date: int = None, revoke_messages: bool = None) -> Ok:
        """
        description Bans a member in a chat; requires can_restrict_members administrator right. Members can't be banned in private or secret chats. In supergroups and channels, the user will not be able to return to the group on their own using invite links, etc., unless unbanned first
        chat_id Chat identifier
        member_id Member identifier
        banned_until_date Point in time (Unix timestamp) when the user will be unbanned; 0 if never. If the user is banned for more than 366 days or for less than 30 seconds from the current time, the user is considered to be banned forever. Ignored in basic groups and if a chat is banned
        revoke_messages Pass true to delete all messages in the chat for the user who is being removed. Always true for supergroups and channels
        """
        return await self._client.call_method('banChatMember', {'@type': 'banChatMember', 'chat_id': chat_id, 'member_id': member_id, 'banned_until_date': banned_until_date, 'revoke_messages': revoke_messages})

    async def can_transfer_ownership(self) -> CanTransferOwnershipResult:
        """
        description Checks whether the current session can be used to transfer a chat ownership to another user
        """
        return await self._client.call_method('canTransferOwnership', {'@type': 'canTransferOwnership'})

    async def transfer_chat_ownership(self, chat_id: int = None, user_id: int = None, password: str = None) -> Ok:
        """
        description Changes the owner of a chat; for basic groups, supergroups and channel chats only; requires owner privileges in the chat. Use the method canTransferOwnership to check whether the ownership can be transferred from the current session
        chat_id Chat identifier
        user_id Identifier of the user to which transfer the ownership. The ownership can't be transferred to a bot or to a deleted user
        password The 2-step verification password of the current user
        """
        return await self._client.call_method('transferChatOwnership', {'@type': 'transferChatOwnership', 'chat_id': chat_id, 'user_id': user_id, 'password': password})

    async def get_chat_owner_after_leaving(self, chat_id: int = None) -> User:
        """
        description Returns the user who will become the owner of the chat after 7 days if the current user does not return to the supergroup or channel during that period or immediately for basic groups; requires owner privileges in the chat.
        chat_id Chat identifier
        """
        return await self._client.call_method('getChatOwnerAfterLeaving', {'@type': 'getChatOwnerAfterLeaving', 'chat_id': chat_id})

    async def get_chat_member(self, chat_id: int = None, member_id: MessageSender = None) -> ChatMember:
        """
        description Returns information about a single member of a chat @chat_id Chat identifier @member_id Member identifier
        """
        return await self._client.call_method('getChatMember', {'@type': 'getChatMember', 'chat_id': chat_id, 'member_id': member_id})

    async def search_chat_members(self, chat_id: int = None, query: str = None, limit: int = None, filter: ChatMembersFilter = None) -> ChatMembers:
        """
        description Searches for a specified query in the first name, last name and usernames of the members of a specified chat. Requires administrator rights if the chat is a channel
        chat_id Chat identifier
        query Query to search for
        limit The maximum number of users to be returned; up to 200
        filter The type of users to search for; pass null to search among all chat members
        """
        return await self._client.call_method('searchChatMembers', {'@type': 'searchChatMembers', 'chat_id': chat_id, 'query': query, 'limit': limit, 'filter': filter})

    async def get_chat_administrators(self, chat_id: int = None) -> ChatAdministrators:
        """
        description Returns a list of administrators of the chat with their custom titles @chat_id Chat identifier
        """
        return await self._client.call_method('getChatAdministrators', {'@type': 'getChatAdministrators', 'chat_id': chat_id})

    async def clear_all_draft_messages(self, exclude_secret_chats: bool = None) -> Ok:
        """
        description Clears message drafts in all chats @exclude_secret_chats Pass true to keep local message drafts in secret chats
        """
        return await self._client.call_method('clearAllDraftMessages', {'@type': 'clearAllDraftMessages', 'exclude_secret_chats': exclude_secret_chats})

    async def get_stake_dice_state(self) -> StakeDiceState:
        """
        description Returns the current state of stake dice
        """
        return await self._client.call_method('getStakeDiceState', {'@type': 'getStakeDiceState'})

    async def get_saved_notification_sound(self, notification_sound_id: int = None) -> NotificationSound:
        """
        description Returns saved notification sound by its identifier. Returns a 404 error if there is no saved notification sound with the specified identifier @notification_sound_id Identifier of the notification sound
        """
        return await self._client.call_method('getSavedNotificationSound', {'@type': 'getSavedNotificationSound', 'notification_sound_id': notification_sound_id})

    async def get_saved_notification_sounds(self) -> NotificationSounds:
        """
        description Returns the list of saved notification sounds. If a sound isn't in the list, then default sound needs to be used
        """
        return await self._client.call_method('getSavedNotificationSounds', {'@type': 'getSavedNotificationSounds'})

    async def add_saved_notification_sound(self, sound: InputFile = None) -> NotificationSound:
        """
        description Adds a new notification sound to the list of saved notification sounds. The new notification sound is added to the top of the list. If it is already in the list, its position isn't changed @sound Notification sound file to add
        """
        return await self._client.call_method('addSavedNotificationSound', {'@type': 'addSavedNotificationSound', 'sound': sound})

    async def remove_saved_notification_sound(self, notification_sound_id: int = None) -> Ok:
        """
        description Removes a notification sound from the list of saved notification sounds @notification_sound_id Identifier of the notification sound
        """
        return await self._client.call_method('removeSavedNotificationSound', {'@type': 'removeSavedNotificationSound', 'notification_sound_id': notification_sound_id})

    async def get_chat_notification_settings_exceptions(self, scope: NotificationSettingsScope = None, compare_sound: bool = None) -> Chats:
        """
        description Returns the list of chats with non-default notification settings for new messages
        scope If specified, only chats from the scope will be returned; pass null to return chats from all scopes
        compare_sound Pass true to include in the response chats with only non-default sound
        """
        return await self._client.call_method('getChatNotificationSettingsExceptions', {'@type': 'getChatNotificationSettingsExceptions', 'scope': scope, 'compare_sound': compare_sound})

    async def get_scope_notification_settings(self, scope: NotificationSettingsScope = None) -> ScopeNotificationSettings:
        """
        description Returns the notification settings for chats of a given type @scope Types of chats for which to return the notification settings information
        """
        return await self._client.call_method('getScopeNotificationSettings', {'@type': 'getScopeNotificationSettings', 'scope': scope})

    async def set_scope_notification_settings(self, scope: NotificationSettingsScope = None, notification_settings: scopeNotificationSettings = None) -> Ok:
        """
        description Changes notification settings for chats of a given type @scope Types of chats for which to change the notification settings @notification_settings The new notification settings for the given scope
        """
        return await self._client.call_method('setScopeNotificationSettings', {'@type': 'setScopeNotificationSettings', 'scope': scope, 'notification_settings': notification_settings})

    async def set_reaction_notification_settings(self, notification_settings: reactionNotificationSettings = None) -> Ok:
        """
        description Changes notification settings for reactions @notification_settings The new notification settings for reactions
        """
        return await self._client.call_method('setReactionNotificationSettings', {'@type': 'setReactionNotificationSettings', 'notification_settings': notification_settings})

    async def reset_all_notification_settings(self) -> Ok:
        """
        description Resets all chat and scope notification settings to their default values. By default, all chats are unmuted and message previews are shown
        """
        return await self._client.call_method('resetAllNotificationSettings', {'@type': 'resetAllNotificationSettings'})

    async def toggle_chat_is_pinned(self, chat_list: ChatList = None, chat_id: int = None, is_pinned: bool = None) -> Ok:
        """
        description Changes the pinned state of a chat. There can be up to getOption("pinned_chat_count_max")/getOption("pinned_archived_chat_count_max") pinned non-secret chats and the same number of secret chats in the main/archive chat list. The limit can be increased with Telegram Premium
        chat_list Chat list in which to change the pinned state of the chat
        chat_id Chat identifier
        is_pinned Pass true to pin the chat; pass false to unpin it
        """
        return await self._client.call_method('toggleChatIsPinned', {'@type': 'toggleChatIsPinned', 'chat_list': chat_list, 'chat_id': chat_id, 'is_pinned': is_pinned})

    async def set_pinned_chats(self, chat_list: ChatList = None, chat_ids: List[int] = None) -> Ok:
        """
        description Changes the order of pinned chats @chat_list Chat list in which to change the order of pinned chats @chat_ids The new list of pinned chats
        """
        return await self._client.call_method('setPinnedChats', {'@type': 'setPinnedChats', 'chat_list': chat_list, 'chat_ids': chat_ids})

    async def read_chat_list(self, chat_list: ChatList = None) -> Ok:
        """
        description Traverses all chats in a chat list and marks all messages in the chats as read @chat_list Chat list in which to mark all chats as read
        """
        return await self._client.call_method('readChatList', {'@type': 'readChatList', 'chat_list': chat_list})

    async def get_current_weather(self, location: location = None) -> CurrentWeather:
        """
        description Returns the current weather in the given location @location The location
        """
        return await self._client.call_method('getCurrentWeather', {'@type': 'getCurrentWeather', 'location': location})

    async def get_story(self, story_poster_chat_id: int = None, story_id: int = None, only_local: bool = None) -> Story:
        """
        description Returns a story
        story_poster_chat_id Identifier of the chat that posted the story
        story_id Story identifier
        only_local Pass true to get only locally available information without sending network requests
        """
        return await self._client.call_method('getStory', {'@type': 'getStory', 'story_poster_chat_id': story_poster_chat_id, 'story_id': story_id, 'only_local': only_local})

    async def get_chats_to_post_stories(self) -> Chats:
        """
        description Returns supergroup and channel chats in which the current user has the right to post stories. The chats must be rechecked with canPostStory before actually trying to post a story there
        """
        return await self._client.call_method('getChatsToPostStories', {'@type': 'getChatsToPostStories'})

    async def can_post_story(self, chat_id: int = None) -> CanPostStoryResult:
        """
        description Checks whether the current user can post a story on behalf of a chat; requires can_post_stories administrator right for supergroup and channel chats
        chat_id Chat identifier. Pass Saved Messages chat identifier when posting a story on behalf of the current user
        """
        return await self._client.call_method('canPostStory', {'@type': 'canPostStory', 'chat_id': chat_id})

    async def post_story(self, chat_id: int = None, content: InputStoryContent = None, areas: inputStoryAreas = None, caption: formattedText = None, privacy_settings: StoryPrivacySettings = None, album_ids: List[int] = None, active_period: int = None, from_story_full_id: storyFullId = None, is_posted_to_chat_page: bool = None, protect_content: bool = None) -> Story:
        """
        description Posts a new story on behalf of a chat; requires can_post_stories administrator right for supergroup and channel chats. Returns a temporary story
        chat_id Identifier of the chat that will post the story. Pass Saved Messages chat identifier when posting a story on behalf of the current user
        content Content of the story
        areas Clickable rectangle areas to be shown on the story media; pass null if none
        caption Story caption; pass null to use an empty caption; 0-getOption("story_caption_length_max") characters; can have entities only if getOption("can_use_text_entities_in_story_caption")
        privacy_settings The privacy settings for the story; ignored for stories posted on behalf of supergroup and channel chats
        album_ids Identifiers of story albums to which the story will be added upon posting. An album can have up to getOption("story_album_size_max") stories
        active_period Period after which the story is moved to archive, in seconds; must be one of 6 * 3600, 12 * 3600, 86400, or 2 * 86400 for Telegram Premium users, and 86400 otherwise
        from_story_full_id Full identifier of the original story, which content was used to create the story; pass null if the story isn't repost of another story
        is_posted_to_chat_page Pass true to keep the story accessible after expiration
        protect_content Pass true if the content of the story must be protected from forwarding and screenshotting
        """
        return await self._client.call_method('postStory', {'@type': 'postStory', 'chat_id': chat_id, 'content': content, 'areas': areas, 'caption': caption, 'privacy_settings': privacy_settings, 'album_ids': album_ids, 'active_period': active_period, 'from_story_full_id': from_story_full_id, 'is_posted_to_chat_page': is_posted_to_chat_page, 'protect_content': protect_content})

    async def start_live_story(self, chat_id: int = None, privacy_settings: StoryPrivacySettings = None, protect_content: bool = None, is_rtmp_stream: bool = None, enable_messages: bool = None, paid_message_star_count: int = None) -> StartLiveStoryResult:
        """
        description Starts a new live story on behalf of a chat; requires can_post_stories administrator right for channel chats
        chat_id Identifier of the chat that will start the live story. Pass Saved Messages chat identifier when starting a live story on behalf of the current user, or a channel chat identifier
        privacy_settings The privacy settings for the story; ignored for stories posted on behalf of channel chats
        protect_content Pass true if the content of the story must be protected from screenshotting
        is_rtmp_stream Pass true to create an RTMP stream instead of an ordinary group call
        enable_messages Pass true to allow viewers of the story to send messages
        paid_message_star_count The minimum number of Telegram Stars that must be paid by viewers for each sent message to the call; 0-getOption("paid_group_call_message_star_count_max")
        """
        return await self._client.call_method('startLiveStory', {'@type': 'startLiveStory', 'chat_id': chat_id, 'privacy_settings': privacy_settings, 'protect_content': protect_content, 'is_rtmp_stream': is_rtmp_stream, 'enable_messages': enable_messages, 'paid_message_star_count': paid_message_star_count})

    async def edit_story(self, story_poster_chat_id: int = None, story_id: int = None, content: InputStoryContent = None, areas: inputStoryAreas = None, caption: formattedText = None) -> Ok:
        """
        description Changes content and caption of a story. Can be called only if story.can_be_edited == true
        story_poster_chat_id Identifier of the chat that posted the story
        story_id Identifier of the story to edit
        content New content of the story; pass null to keep the current content
        areas New clickable rectangle areas to be shown on the story media; pass null to keep the current areas. Areas can't be edited if story content isn't changed
        caption New story caption; pass null to keep the current caption
        """
        return await self._client.call_method('editStory', {'@type': 'editStory', 'story_poster_chat_id': story_poster_chat_id, 'story_id': story_id, 'content': content, 'areas': areas, 'caption': caption})

    async def edit_story_cover(self, story_poster_chat_id: int = None, story_id: int = None, cover_frame_timestamp: float = None) -> Ok:
        """
        description Changes cover of a video story. Can be called only if story.can_be_edited == true and the story isn't being edited now
        story_poster_chat_id Identifier of the chat that posted the story
        story_id Identifier of the story to edit
        cover_frame_timestamp New timestamp of the frame, which will be used as video thumbnail
        """
        return await self._client.call_method('editStoryCover', {'@type': 'editStoryCover', 'story_poster_chat_id': story_poster_chat_id, 'story_id': story_id, 'cover_frame_timestamp': cover_frame_timestamp})

    async def set_story_privacy_settings(self, story_id: int = None, privacy_settings: StoryPrivacySettings = None) -> Ok:
        """
        description Changes privacy settings of a story. The method can be called only for stories posted on behalf of the current user and if story.can_set_privacy_settings == true
        story_id Identifier of the story
        privacy_settings The new privacy settings for the story
        """
        return await self._client.call_method('setStoryPrivacySettings', {'@type': 'setStoryPrivacySettings', 'story_id': story_id, 'privacy_settings': privacy_settings})

    async def toggle_story_is_posted_to_chat_page(self, story_poster_chat_id: int = None, story_id: int = None, is_posted_to_chat_page: bool = None) -> Ok:
        """
        description Toggles whether a story is accessible after expiration. Can be called only if story.can_toggle_is_posted_to_chat_page == true
        story_poster_chat_id Identifier of the chat that posted the story
        story_id Identifier of the story
        is_posted_to_chat_page Pass true to make the story accessible after expiration; pass false to make it private
        """
        return await self._client.call_method('toggleStoryIsPostedToChatPage', {'@type': 'toggleStoryIsPostedToChatPage', 'story_poster_chat_id': story_poster_chat_id, 'story_id': story_id, 'is_posted_to_chat_page': is_posted_to_chat_page})

    async def delete_story(self, story_poster_chat_id: int = None, story_id: int = None) -> Ok:
        """
        description Deletes a previously posted story. Can be called only if story.can_be_deleted == true
        story_poster_chat_id Identifier of the chat that posted the story
        story_id Identifier of the story to delete
        """
        return await self._client.call_method('deleteStory', {'@type': 'deleteStory', 'story_poster_chat_id': story_poster_chat_id, 'story_id': story_id})

    async def get_story_notification_settings_exceptions(self) -> Chats:
        """
        description Returns the list of chats with non-default notification settings for stories
        """
        return await self._client.call_method('getStoryNotificationSettingsExceptions', {'@type': 'getStoryNotificationSettingsExceptions'})

    async def load_active_stories(self, story_list: StoryList = None) -> Ok:
        """
        description Loads more active stories from a story list. The loaded stories will be sent through updates. Active stories are sorted by
        story_list The story list in which to load active stories
        """
        return await self._client.call_method('loadActiveStories', {'@type': 'loadActiveStories', 'story_list': story_list})

    async def set_chat_active_stories_list(self, chat_id: int = None, story_list: StoryList = None) -> Ok:
        """
        description Changes story list in which stories from the chat are shown @chat_id Identifier of the chat that posted stories @story_list New list for active stories posted by the chat
        """
        return await self._client.call_method('setChatActiveStoriesList', {'@type': 'setChatActiveStoriesList', 'chat_id': chat_id, 'story_list': story_list})

    async def get_chat_active_stories(self, chat_id: int = None) -> ChatActiveStories:
        """
        description Returns the list of active stories posted by the given chat @chat_id Chat identifier
        """
        return await self._client.call_method('getChatActiveStories', {'@type': 'getChatActiveStories', 'chat_id': chat_id})

    async def get_chat_posted_to_chat_page_stories(self, chat_id: int = None, from_story_id: int = None, limit: int = None) -> Stories:
        """
        description Returns the list of stories that posted by the given chat to its chat page. If from_story_id == 0, then pinned stories are returned first.
        chat_id Chat identifier
        from_story_id Identifier of the story starting from which stories must be returned; use 0 to get results from pinned and the newest story
        limit The maximum number of stories to be returned.
        """
        return await self._client.call_method('getChatPostedToChatPageStories', {'@type': 'getChatPostedToChatPageStories', 'chat_id': chat_id, 'from_story_id': from_story_id, 'limit': limit})

    async def get_chat_archived_stories(self, chat_id: int = None, from_story_id: int = None, limit: int = None) -> Stories:
        """
        description Returns the list of all stories posted by the given chat; requires can_edit_stories administrator right in the chat.
        chat_id Chat identifier
        from_story_id Identifier of the story starting from which stories must be returned; use 0 to get results from the last story
        limit The maximum number of stories to be returned.
        """
        return await self._client.call_method('getChatArchivedStories', {'@type': 'getChatArchivedStories', 'chat_id': chat_id, 'from_story_id': from_story_id, 'limit': limit})

    async def set_chat_pinned_stories(self, chat_id: int = None, story_ids: List[int] = None) -> Ok:
        """
        description Changes the list of pinned stories on a chat page; requires can_edit_stories administrator right in the chat
        chat_id Identifier of the chat that posted the stories
        story_ids New list of pinned stories. All stories must be posted to the chat page first. There can be up to getOption("pinned_story_count_max") pinned stories on a chat page
        """
        return await self._client.call_method('setChatPinnedStories', {'@type': 'setChatPinnedStories', 'chat_id': chat_id, 'story_ids': story_ids})

    async def open_story(self, story_poster_chat_id: int = None, story_id: int = None) -> Ok:
        """
        description Informs TDLib that a story is opened and is being viewed by the user
        story_poster_chat_id The identifier of the chat that posted the opened story
        story_id The identifier of the story
        """
        return await self._client.call_method('openStory', {'@type': 'openStory', 'story_poster_chat_id': story_poster_chat_id, 'story_id': story_id})

    async def close_story(self, story_poster_chat_id: int = None, story_id: int = None) -> Ok:
        """
        description Informs TDLib that a story is closed by the user
        story_poster_chat_id The identifier of the poster of the story to close
        story_id The identifier of the story
        """
        return await self._client.call_method('closeStory', {'@type': 'closeStory', 'story_poster_chat_id': story_poster_chat_id, 'story_id': story_id})

    async def get_story_available_reactions(self, row_size: int = None) -> AvailableReactions:
        """
        description Returns reactions, which can be chosen for a story @row_size Number of reaction per row, 5-25
        """
        return await self._client.call_method('getStoryAvailableReactions', {'@type': 'getStoryAvailableReactions', 'row_size': row_size})

    async def set_story_reaction(self, story_poster_chat_id: int = None, story_id: int = None, reaction_type: ReactionType = None, update_recent_reactions: bool = None) -> Ok:
        """
        description Changes chosen reaction on a story that has already been sent; not supported for live stories
        story_poster_chat_id The identifier of the poster of the story
        story_id The identifier of the story
        reaction_type Type of the reaction to set; pass null to remove the reaction. Custom emoji reactions can be used only by Telegram Premium users. Paid reactions can't be set
        update_recent_reactions Pass true if the reaction needs to be added to recent reactions
        """
        return await self._client.call_method('setStoryReaction', {'@type': 'setStoryReaction', 'story_poster_chat_id': story_poster_chat_id, 'story_id': story_id, 'reaction_type': reaction_type, 'update_recent_reactions': update_recent_reactions})

    async def get_story_interactions(self, story_id: int = None, query: str = None, only_contacts: bool = None, prefer_forwards: bool = None, prefer_with_reaction: bool = None, offset: str = None, limit: int = None) -> StoryInteractions:
        """
        description Returns interactions with a story. The method can be called only for stories posted on behalf of the current user
        story_id Story identifier
        query Query to search for in names, usernames and titles; may be empty to get all relevant interactions
        only_contacts Pass true to get only interactions by contacts; pass false to get all relevant interactions
        prefer_forwards Pass true to get forwards and reposts first, then reactions, then other views; pass false to get interactions sorted just by interaction date
        prefer_with_reaction Pass true to get interactions with reaction first; pass false to get interactions sorted just by interaction date. Ignored if prefer_forwards == true
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of story interactions to return
        """
        return await self._client.call_method('getStoryInteractions', {'@type': 'getStoryInteractions', 'story_id': story_id, 'query': query, 'only_contacts': only_contacts, 'prefer_forwards': prefer_forwards, 'prefer_with_reaction': prefer_with_reaction, 'offset': offset, 'limit': limit})

    async def get_chat_story_interactions(self, story_poster_chat_id: int = None, story_id: int = None, reaction_type: ReactionType = None, prefer_forwards: bool = None, offset: str = None, limit: int = None) -> StoryInteractions:
        """
        description Returns interactions with a story posted in a chat. Can be used only if story is posted on behalf of a chat and the user is an administrator in the chat
        story_poster_chat_id The identifier of the poster of the story
        story_id Story identifier
        reaction_type Pass the default heart reaction or a suggested reaction type to receive only interactions with the specified reaction type; pass null to receive all interactions; reactionTypePaid isn't supported
        prefer_forwards Pass true to get forwards and reposts first, then reactions, then other views; pass false to get interactions sorted just by interaction date
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of story interactions to return
        """
        return await self._client.call_method('getChatStoryInteractions', {'@type': 'getChatStoryInteractions', 'story_poster_chat_id': story_poster_chat_id, 'story_id': story_id, 'reaction_type': reaction_type, 'prefer_forwards': prefer_forwards, 'offset': offset, 'limit': limit})

    async def report_story(self, story_poster_chat_id: int = None, story_id: int = None, option_id: bytes = None, text: str = None) -> ReportStoryResult:
        """
        description Reports a story to the Telegram moderators
        story_poster_chat_id The identifier of the poster of the story to report
        story_id The identifier of the story to report
        option_id Option identifier chosen by the user; leave empty for the initial request
        text Additional report details; 0-1024 characters; leave empty for the initial request
        """
        return await self._client.call_method('reportStory', {'@type': 'reportStory', 'story_poster_chat_id': story_poster_chat_id, 'story_id': story_id, 'option_id': option_id, 'text': text})

    async def activate_story_stealth_mode(self) -> Ok:
        """
        description Activates stealth mode for stories, which hides all views of stories from the current user in the last "story_stealth_mode_past_period" seconds
        """
        return await self._client.call_method('activateStoryStealthMode', {'@type': 'activateStoryStealthMode'})

    async def get_story_public_forwards(self, story_poster_chat_id: int = None, story_id: int = None, offset: str = None, limit: int = None) -> PublicForwards:
        """
        description Returns forwards of a story as a message to public chats and reposts by public channels. Can be used only if the story is posted on behalf of the current user or story.can_get_statistics == true.
        story_poster_chat_id The identifier of the poster of the story
        story_id The identifier of the story
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of messages and stories to be returned; must be positive and can't be greater than 100. For optimal performance, the number of returned objects is chosen by TDLib and can be smaller than the specified limit
        """
        return await self._client.call_method('getStoryPublicForwards', {'@type': 'getStoryPublicForwards', 'story_poster_chat_id': story_poster_chat_id, 'story_id': story_id, 'offset': offset, 'limit': limit})

    async def get_chat_story_albums(self, chat_id: int = None) -> StoryAlbums:
        """
        description Returns the list of story albums owned by the given chat @chat_id Chat identifier
        """
        return await self._client.call_method('getChatStoryAlbums', {'@type': 'getChatStoryAlbums', 'chat_id': chat_id})

    async def get_story_album_stories(self, chat_id: int = None, story_album_id: int = None, offset: int = None, limit: int = None) -> Stories:
        """
        description Returns the list of stories added to the given story album. For optimal performance, the number of returned stories is chosen by TDLib
        chat_id Chat identifier
        story_album_id Story album identifier
        offset Offset of the first entry to return; use 0 to get results from the first album story
        limit The maximum number of stories to be returned. For optimal performance, the number of returned stories is chosen by TDLib and can be smaller than the specified limit
        """
        return await self._client.call_method('getStoryAlbumStories', {'@type': 'getStoryAlbumStories', 'chat_id': chat_id, 'story_album_id': story_album_id, 'offset': offset, 'limit': limit})

    async def create_story_album(self, story_poster_chat_id: int = None, name: str = None, story_ids: List[int] = None) -> StoryAlbum:
        """
        description Creates an album of stories; requires can_edit_stories administrator right for supergroup and channel chats
        story_poster_chat_id Identifier of the chat that posted the stories
        name Name of the album; 1-12 characters
        story_ids Identifiers of stories to add to the album; 0-getOption("story_album_size_max") identifiers
        """
        return await self._client.call_method('createStoryAlbum', {'@type': 'createStoryAlbum', 'story_poster_chat_id': story_poster_chat_id, 'name': name, 'story_ids': story_ids})

    async def reorder_story_albums(self, chat_id: int = None, story_album_ids: List[int] = None) -> Ok:
        """
        description Changes order of story albums. If the albums are owned by a supergroup or a channel chat, then requires can_edit_stories administrator right in the chat
        chat_id Identifier of the chat that owns the stories
        story_album_ids New order of story albums
        """
        return await self._client.call_method('reorderStoryAlbums', {'@type': 'reorderStoryAlbums', 'chat_id': chat_id, 'story_album_ids': story_album_ids})

    async def delete_story_album(self, chat_id: int = None, story_album_id: int = None) -> Ok:
        """
        description Deletes a story album. If the album is owned by a supergroup or a channel chat, then requires can_edit_stories administrator right in the chat
        chat_id Identifier of the chat that owns the stories
        story_album_id Identifier of the story album
        """
        return await self._client.call_method('deleteStoryAlbum', {'@type': 'deleteStoryAlbum', 'chat_id': chat_id, 'story_album_id': story_album_id})

    async def set_story_album_name(self, chat_id: int = None, story_album_id: int = None, name: str = None) -> StoryAlbum:
        """
        description Changes name of an album of stories. If the album is owned by a supergroup or a channel chat, then requires can_edit_stories administrator right in the chat. Returns the changed album
        chat_id Identifier of the chat that owns the stories
        story_album_id Identifier of the story album
        name New name of the album; 1-12 characters
        """
        return await self._client.call_method('setStoryAlbumName', {'@type': 'setStoryAlbumName', 'chat_id': chat_id, 'story_album_id': story_album_id, 'name': name})

    async def add_story_album_stories(self, chat_id: int = None, story_album_id: int = None, story_ids: List[int] = None) -> StoryAlbum:
        """
        description Adds stories to the beginning of a previously created story album. If the album is owned by a supergroup or a channel chat, then
        chat_id Identifier of the chat that owns the stories
        story_album_id Identifier of the story album
        story_ids Identifier of the stories to add to the album; 1-getOption("story_album_size_max") identifiers.
        """
        return await self._client.call_method('addStoryAlbumStories', {'@type': 'addStoryAlbumStories', 'chat_id': chat_id, 'story_album_id': story_album_id, 'story_ids': story_ids})

    async def remove_story_album_stories(self, chat_id: int = None, story_album_id: int = None, story_ids: List[int] = None) -> StoryAlbum:
        """
        description Removes stories from an album. If the album is owned by a supergroup or a channel chat, then
        chat_id Identifier of the chat that owns the stories
        story_album_id Identifier of the story album
        story_ids Identifier of the stories to remove from the album
        """
        return await self._client.call_method('removeStoryAlbumStories', {'@type': 'removeStoryAlbumStories', 'chat_id': chat_id, 'story_album_id': story_album_id, 'story_ids': story_ids})

    async def reorder_story_album_stories(self, chat_id: int = None, story_album_id: int = None, story_ids: List[int] = None) -> StoryAlbum:
        """
        description Changes order of stories in an album. If the album is owned by a supergroup or a channel chat, then
        chat_id Identifier of the chat that owns the stories
        story_album_id Identifier of the story album
        story_ids Identifier of the stories to move to the beginning of the album. All other stories are placed in the current order after the specified stories
        """
        return await self._client.call_method('reorderStoryAlbumStories', {'@type': 'reorderStoryAlbumStories', 'chat_id': chat_id, 'story_album_id': story_album_id, 'story_ids': story_ids})

    async def get_chat_boost_level_features(self, is_channel: bool = None, level: int = None) -> ChatBoostLevelFeatures:
        """
        description Returns the list of features available on the specific chat boost level. This is an offline method
        is_channel Pass true to get the list of features for channels; pass false to get the list of features for supergroups
        level Chat boost level
        """
        return await self._client.call_method('getChatBoostLevelFeatures', {'@type': 'getChatBoostLevelFeatures', 'is_channel': is_channel, 'level': level})

    async def get_chat_boost_features(self, is_channel: bool = None) -> ChatBoostFeatures:
        """
        description Returns the list of features available for different chat boost levels. This is an offline method
        is_channel Pass true to get the list of features for channels; pass false to get the list of features for supergroups
        """
        return await self._client.call_method('getChatBoostFeatures', {'@type': 'getChatBoostFeatures', 'is_channel': is_channel})

    async def get_available_chat_boost_slots(self) -> ChatBoostSlots:
        """
        description Returns the list of available chat boost slots for the current user
        """
        return await self._client.call_method('getAvailableChatBoostSlots', {'@type': 'getAvailableChatBoostSlots'})

    async def get_chat_boost_status(self, chat_id: int = None) -> ChatBoostStatus:
        """
        description Returns the current boost status for a supergroup or a channel chat @chat_id Identifier of the chat
        """
        return await self._client.call_method('getChatBoostStatus', {'@type': 'getChatBoostStatus', 'chat_id': chat_id})

    async def boost_chat(self, chat_id: int = None, slot_ids: List[int] = None) -> ChatBoostSlots:
        """
        description Boosts a chat and returns the list of available chat boost slots for the current user after the boost
        chat_id Identifier of the chat
        slot_ids Identifiers of boost slots of the current user from which to apply boosts to the chat
        """
        return await self._client.call_method('boostChat', {'@type': 'boostChat', 'chat_id': chat_id, 'slot_ids': slot_ids})

    async def get_chat_boost_link(self, chat_id: int = None) -> ChatBoostLink:
        """
        description Returns an HTTPS link to boost the specified supergroup or channel chat @chat_id Identifier of the chat
        """
        return await self._client.call_method('getChatBoostLink', {'@type': 'getChatBoostLink', 'chat_id': chat_id})

    async def get_chat_boost_link_info(self, url: str = None) -> ChatBoostLinkInfo:
        """
        description Returns information about a link to boost a chat. Can be called for any internal link of the type internalLinkTypeChatBoost @url The link to boost a chat
        """
        return await self._client.call_method('getChatBoostLinkInfo', {'@type': 'getChatBoostLinkInfo', 'url': url})

    async def get_chat_boosts(self, chat_id: int = None, only_gift_codes: bool = None, offset: str = None, limit: int = None) -> FoundChatBoosts:
        """
        description Returns the list of boosts applied to a chat; requires administrator rights in the chat
        chat_id Identifier of the chat
        only_gift_codes Pass true to receive only boosts received from gift codes and giveaways created by the chat
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of boosts to be returned; up to 100. For optimal performance, the number of returned boosts can be smaller than the specified limit
        """
        return await self._client.call_method('getChatBoosts', {'@type': 'getChatBoosts', 'chat_id': chat_id, 'only_gift_codes': only_gift_codes, 'offset': offset, 'limit': limit})

    async def get_user_chat_boosts(self, chat_id: int = None, user_id: int = None) -> FoundChatBoosts:
        """
        description Returns the list of boosts applied to a chat by a given user; requires administrator rights in the chat; for bots only
        chat_id Identifier of the chat
        user_id Identifier of the user
        """
        return await self._client.call_method('getUserChatBoosts', {'@type': 'getUserChatBoosts', 'chat_id': chat_id, 'user_id': user_id})

    async def get_attachment_menu_bot(self, bot_user_id: int = None) -> AttachmentMenuBot:
        """
        description Returns information about a bot that can be added to attachment or side menu @bot_user_id Bot's user identifier
        """
        return await self._client.call_method('getAttachmentMenuBot', {'@type': 'getAttachmentMenuBot', 'bot_user_id': bot_user_id})

    async def toggle_bot_is_added_to_attachment_menu(self, bot_user_id: int = None, is_added: bool = None, allow_write_access: bool = None) -> Ok:
        """
        description Adds or removes a bot to attachment and side menu. Bot can be added to the menu, only if userTypeBot.can_be_added_to_attachment_menu == true
        bot_user_id Bot's user identifier
        is_added Pass true to add the bot to attachment menu; pass false to remove the bot from attachment menu
        allow_write_access Pass true if the current user allowed the bot to send them messages. Ignored if is_added is false
        """
        return await self._client.call_method('toggleBotIsAddedToAttachmentMenu', {'@type': 'toggleBotIsAddedToAttachmentMenu', 'bot_user_id': bot_user_id, 'is_added': is_added, 'allow_write_access': allow_write_access})

    async def get_themed_emoji_statuses(self) -> EmojiStatusCustomEmojis:
        """
        description Returns up to 8 emoji statuses, which must be shown right after the default Premium Badge in the emoji status list for self status
        """
        return await self._client.call_method('getThemedEmojiStatuses', {'@type': 'getThemedEmojiStatuses'})

    async def get_recent_emoji_statuses(self) -> EmojiStatuses:
        """
        description Returns recent emoji statuses for self status
        """
        return await self._client.call_method('getRecentEmojiStatuses', {'@type': 'getRecentEmojiStatuses'})

    async def get_upgraded_gift_emoji_statuses(self) -> EmojiStatuses:
        """
        description Returns available upgraded gift emoji statuses for self status
        """
        return await self._client.call_method('getUpgradedGiftEmojiStatuses', {'@type': 'getUpgradedGiftEmojiStatuses'})

    async def get_default_emoji_statuses(self) -> EmojiStatusCustomEmojis:
        """
        description Returns default emoji statuses for self status
        """
        return await self._client.call_method('getDefaultEmojiStatuses', {'@type': 'getDefaultEmojiStatuses'})

    async def clear_recent_emoji_statuses(self) -> Ok:
        """
        description Clears the list of recently used emoji statuses for self status
        """
        return await self._client.call_method('clearRecentEmojiStatuses', {'@type': 'clearRecentEmojiStatuses'})

    async def get_themed_chat_emoji_statuses(self) -> EmojiStatusCustomEmojis:
        """
        description Returns up to 8 emoji statuses, which must be shown in the emoji status list for chats
        """
        return await self._client.call_method('getThemedChatEmojiStatuses', {'@type': 'getThemedChatEmojiStatuses'})

    async def get_default_chat_emoji_statuses(self) -> EmojiStatusCustomEmojis:
        """
        description Returns default emoji statuses for chats
        """
        return await self._client.call_method('getDefaultChatEmojiStatuses', {'@type': 'getDefaultChatEmojiStatuses'})

    async def get_disallowed_chat_emoji_statuses(self) -> EmojiStatusCustomEmojis:
        """
        description Returns the list of emoji statuses, which can't be used as chat emoji status, even if they are from a sticker set with is_allowed_as_chat_emoji_status == true
        """
        return await self._client.call_method('getDisallowedChatEmojiStatuses', {'@type': 'getDisallowedChatEmojiStatuses'})

    async def download_file(self, file_id: int = None, priority: int = None, offset: int = None, limit: int = None, synchronous: bool = None) -> File:
        """
        description Downloads a file from the cloud. Download progress and completion of the download will be notified through updateFile updates
        file_id Identifier of the file to download
        priority Priority of the download (1-32). The higher the priority, the earlier the file will be downloaded. If the priorities of two files are equal, then the last one for which downloadFile/addFileToDownloads was called will be downloaded first
        offset The starting position from which the file needs to be downloaded
        limit Number of bytes which need to be downloaded starting from the "offset" position before the download will automatically be canceled; use 0 to download without a limit
        synchronous Pass true to return response only after the file download has succeeded, has failed, has been canceled, or a new downloadFile request with different offset/limit parameters was sent; pass false to return file state immediately, just after the download has been started
        """
        return await self._client.call_method('downloadFile', {'@type': 'downloadFile', 'file_id': file_id, 'priority': priority, 'offset': offset, 'limit': limit, 'synchronous': synchronous})

    async def get_file_downloaded_prefix_size(self, file_id: int = None, offset: int = None) -> FileDownloadedPrefixSize:
        """
        description Returns file downloaded prefix size from a given offset, in bytes @file_id Identifier of the file @offset Offset from which downloaded prefix size needs to be calculated
        """
        return await self._client.call_method('getFileDownloadedPrefixSize', {'@type': 'getFileDownloadedPrefixSize', 'file_id': file_id, 'offset': offset})

    async def cancel_download_file(self, file_id: int = None, only_if_pending: bool = None) -> Ok:
        """
        description Stops the downloading of a file. If a file has already been downloaded, does nothing @file_id Identifier of a file to stop downloading @only_if_pending Pass true to stop downloading only if it hasn't been started, i.e. request hasn't been sent to server
        """
        return await self._client.call_method('cancelDownloadFile', {'@type': 'cancelDownloadFile', 'file_id': file_id, 'only_if_pending': only_if_pending})

    async def get_suggested_file_name(self, file_id: int = None, directory: str = None) -> Text:
        """
        description Returns suggested name for saving a file in a given directory @file_id Identifier of the file @directory Directory in which the file is expected to be saved
        """
        return await self._client.call_method('getSuggestedFileName', {'@type': 'getSuggestedFileName', 'file_id': file_id, 'directory': directory})

    async def preliminary_upload_file(self, file: InputFile = None, file_type: FileType = None, priority: int = None) -> File:
        """
        description Preliminarily uploads a file to the cloud before sending it in a message, which can be useful for uploading of being recorded voice and video notes.
        file File to upload
        file_type File type; pass null if unknown
        priority Priority of the upload (1-32). The higher the priority, the earlier the file will be uploaded. If the priorities of two files are equal, then the first one for which preliminaryUploadFile was called will be uploaded first
        """
        return await self._client.call_method('preliminaryUploadFile', {'@type': 'preliminaryUploadFile', 'file': file, 'file_type': file_type, 'priority': priority})

    async def cancel_preliminary_upload_file(self, file_id: int = None) -> Ok:
        """
        description Stops the preliminary uploading of a file. Supported only for files uploaded by using preliminaryUploadFile @file_id Identifier of the file to stop uploading
        """
        return await self._client.call_method('cancelPreliminaryUploadFile', {'@type': 'cancelPreliminaryUploadFile', 'file_id': file_id})

    async def write_generated_file_part(self, generation_id: int = None, offset: int = None, data: bytes = None) -> Ok:
        """
        description Writes a part of a generated file. This method is intended to be used only if the application has no direct access to TDLib's file system, because it is usually slower than a direct write to the destination file
        generation_id The identifier of the generation process
        offset The offset from which to write the data to the file
        data The data to write
        """
        return await self._client.call_method('writeGeneratedFilePart', {'@type': 'writeGeneratedFilePart', 'generation_id': generation_id, 'offset': offset, 'data': data})

    async def set_file_generation_progress(self, generation_id: int = None, expected_size: int = None, local_prefix_size: int = None) -> Ok:
        """
        description Informs TDLib on a file generation progress
        generation_id The identifier of the generation process
        expected_size Expected size of the generated file, in bytes; 0 if unknown
        local_prefix_size The number of bytes already generated
        """
        return await self._client.call_method('setFileGenerationProgress', {'@type': 'setFileGenerationProgress', 'generation_id': generation_id, 'expected_size': expected_size, 'local_prefix_size': local_prefix_size})

    async def finish_file_generation(self, generation_id: int = None, error: error = None) -> Ok:
        """
        description Finishes the file generation
        generation_id The identifier of the generation process
        error If passed, the file generation has failed and must be terminated; pass null if the file generation succeeded
        """
        return await self._client.call_method('finishFileGeneration', {'@type': 'finishFileGeneration', 'generation_id': generation_id, 'error': error})

    async def read_file_part(self, file_id: int = None, offset: int = None, count: int = None) -> Data:
        """
        description Reads a part of a file from the TDLib file cache and returns read bytes. This method is intended to be used only if the application has no direct access to TDLib's file system, because it is usually slower than a direct read from the file
        file_id Identifier of the file. The file must be located in the TDLib file cache
        offset The offset from which to read the file
        count Number of bytes to read. An error will be returned if there are not enough bytes available in the file from the specified position. Pass 0 to read all available data from the specified position
        """
        return await self._client.call_method('readFilePart', {'@type': 'readFilePart', 'file_id': file_id, 'offset': offset, 'count': count})

    async def delete_file(self, file_id: int = None) -> Ok:
        """
        description Deletes a file from the TDLib file cache @file_id Identifier of the file to delete
        """
        return await self._client.call_method('deleteFile', {'@type': 'deleteFile', 'file_id': file_id})

    async def add_file_to_downloads(self, file_id: int = None, chat_id: int = None, message_id: int = None, priority: int = None) -> File:
        """
        description Adds a file from a message to the list of file downloads. Download progress and completion of the download will be notified through updateFile updates.
        file_id Identifier of the file to download
        chat_id Chat identifier of the message with the file
        message_id Message identifier
        priority Priority of the download (1-32). The higher the priority, the earlier the file will be downloaded. If the priorities of two files are equal, then the last one for which downloadFile/addFileToDownloads was called will be downloaded first
        """
        return await self._client.call_method('addFileToDownloads', {'@type': 'addFileToDownloads', 'file_id': file_id, 'chat_id': chat_id, 'message_id': message_id, 'priority': priority})

    async def toggle_download_is_paused(self, file_id: int = None, is_paused: bool = None) -> Ok:
        """
        description Changes pause state of a file in the file download list
        file_id Identifier of the downloaded file
        is_paused Pass true if the download is paused
        """
        return await self._client.call_method('toggleDownloadIsPaused', {'@type': 'toggleDownloadIsPaused', 'file_id': file_id, 'is_paused': is_paused})

    async def toggle_all_downloads_are_paused(self, are_paused: bool = None) -> Ok:
        """
        description Changes pause state of all files in the file download list @are_paused Pass true to pause all downloads; pass false to unpause them
        """
        return await self._client.call_method('toggleAllDownloadsArePaused', {'@type': 'toggleAllDownloadsArePaused', 'are_paused': are_paused})

    async def remove_file_from_downloads(self, file_id: int = None, delete_from_cache: bool = None) -> Ok:
        """
        description Removes a file from the file download list @file_id Identifier of the downloaded file @delete_from_cache Pass true to delete the file from the TDLib file cache
        """
        return await self._client.call_method('removeFileFromDownloads', {'@type': 'removeFileFromDownloads', 'file_id': file_id, 'delete_from_cache': delete_from_cache})

    async def remove_all_files_from_downloads(self, only_active: bool = None, only_completed: bool = None, delete_from_cache: bool = None) -> Ok:
        """
        description Removes all files from the file download list
        only_active Pass true to remove only active downloads, including paused
        only_completed Pass true to remove only completed downloads
        delete_from_cache Pass true to delete the file from the TDLib file cache
        """
        return await self._client.call_method('removeAllFilesFromDownloads', {'@type': 'removeAllFilesFromDownloads', 'only_active': only_active, 'only_completed': only_completed, 'delete_from_cache': delete_from_cache})

    async def search_file_downloads(self, query: str = None, only_active: bool = None, only_completed: bool = None, offset: str = None, limit: int = None) -> FoundFileDownloads:
        """
        description Searches for files in the file download list or recently downloaded files from the list
        query Query to search for; may be empty to return all downloaded files
        only_active Pass true to search only for active downloads, including paused
        only_completed Pass true to search only for completed downloads
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of files to be returned
        """
        return await self._client.call_method('searchFileDownloads', {'@type': 'searchFileDownloads', 'query': query, 'only_active': only_active, 'only_completed': only_completed, 'offset': offset, 'limit': limit})

    async def set_application_verification_token(self, verification_id: int = None, token: str = None) -> Ok:
        """
        description Informs TDLib that application or reCAPTCHA verification has been completed. Can be called before authorization
        verification_id Unique identifier for the verification process as received from updateApplicationVerificationRequired or updateApplicationRecaptchaVerificationRequired
        token Play Integrity API token for the Android application, or secret from push notification for the iOS application for application verification, or reCAPTCHA token for reCAPTCHA verifications;
        """
        return await self._client.call_method('setApplicationVerificationToken', {'@type': 'setApplicationVerificationToken', 'verification_id': verification_id, 'token': token})

    async def get_message_file_type(self, message_file_head: str = None) -> MessageFileType:
        """
        description Returns information about a file with messages exported from another application @message_file_head Beginning of the message file; up to 100 first lines
        """
        return await self._client.call_method('getMessageFileType', {'@type': 'getMessageFileType', 'message_file_head': message_file_head})

    async def get_message_import_confirmation_text(self, chat_id: int = None) -> Text:
        """
        description Returns a confirmation text to be shown to the user before starting message import
        chat_id Identifier of a chat to which the messages will be imported. It must be an identifier of a private chat with a mutual contact or an identifier of a supergroup chat with can_change_info member right
        """
        return await self._client.call_method('getMessageImportConfirmationText', {'@type': 'getMessageImportConfirmationText', 'chat_id': chat_id})

    async def import_messages(self, chat_id: int = None, message_file: InputFile = None, attached_files: List[InputFile] = None) -> Ok:
        """
        description Imports messages exported from another application
        chat_id Identifier of a chat to which the messages will be imported. It must be an identifier of a private chat with a mutual contact or an identifier of a supergroup chat with can_change_info member right
        message_file File with messages to import. Only inputFileLocal and inputFileGenerated are supported. The file must not be previously uploaded
        attached_files Files used in the imported messages. Only inputFileLocal and inputFileGenerated are supported. The files must not be previously uploaded
        """
        return await self._client.call_method('importMessages', {'@type': 'importMessages', 'chat_id': chat_id, 'message_file': message_file, 'attached_files': attached_files})

    async def replace_primary_chat_invite_link(self, chat_id: int = None) -> ChatInviteLink:
        """
        description Replaces current primary invite link for a chat with a new primary invite link. Available for basic groups, supergroups, and channels. Requires administrator privileges and can_invite_users right @chat_id Chat identifier
        """
        return await self._client.call_method('replacePrimaryChatInviteLink', {'@type': 'replacePrimaryChatInviteLink', 'chat_id': chat_id})

    async def create_chat_invite_link(self, chat_id: int = None, name: str = None, expiration_date: int = None, member_limit: int = None, creates_join_request: bool = None) -> ChatInviteLink:
        """
        description Creates a new invite link for a chat. Available for basic groups, supergroups, and channels. Requires administrator privileges and can_invite_users right in the chat
        chat_id Chat identifier
        name Invite link name; 0-32 characters
        expiration_date Point in time (Unix timestamp) when the link will expire; pass 0 if never
        member_limit The maximum number of chat members that can join the chat via the link simultaneously; 0-99999; pass 0 if not limited
        creates_join_request Pass true if users joining the chat via the link need to be approved by chat administrators. In this case, member_limit must be 0
        """
        return await self._client.call_method('createChatInviteLink', {'@type': 'createChatInviteLink', 'chat_id': chat_id, 'name': name, 'expiration_date': expiration_date, 'member_limit': member_limit, 'creates_join_request': creates_join_request})

    async def create_chat_subscription_invite_link(self, chat_id: int = None, name: str = None, subscription_pricing: starSubscriptionPricing = None) -> ChatInviteLink:
        """
        description Creates a new subscription invite link for a channel chat. Requires can_invite_users right in the chat
        chat_id Chat identifier
        name Invite link name; 0-32 characters
        subscription_pricing Information about subscription plan that will be applied to the users joining the chat via the link.
        """
        return await self._client.call_method('createChatSubscriptionInviteLink', {'@type': 'createChatSubscriptionInviteLink', 'chat_id': chat_id, 'name': name, 'subscription_pricing': subscription_pricing})

    async def edit_chat_invite_link(self, chat_id: int = None, invite_link: str = None, name: str = None, expiration_date: int = None, member_limit: int = None, creates_join_request: bool = None) -> ChatInviteLink:
        """
        description Edits a non-primary invite link for a chat. Available for basic groups, supergroups, and channels.
        chat_id Chat identifier
        invite_link Invite link to be edited
        name Invite link name; 0-32 characters
        expiration_date Point in time (Unix timestamp) when the link will expire; pass 0 if never
        member_limit The maximum number of chat members that can join the chat via the link simultaneously; 0-99999; pass 0 if not limited
        creates_join_request Pass true if users joining the chat via the link need to be approved by chat administrators. In this case, member_limit must be 0
        """
        return await self._client.call_method('editChatInviteLink', {'@type': 'editChatInviteLink', 'chat_id': chat_id, 'invite_link': invite_link, 'name': name, 'expiration_date': expiration_date, 'member_limit': member_limit, 'creates_join_request': creates_join_request})

    async def edit_chat_subscription_invite_link(self, chat_id: int = None, invite_link: str = None, name: str = None) -> ChatInviteLink:
        """
        description Edits a subscription invite link for a channel chat. Requires can_invite_users right in the chat for own links and owner privileges for other links
        chat_id Chat identifier
        invite_link Invite link to be edited
        name Invite link name; 0-32 characters
        """
        return await self._client.call_method('editChatSubscriptionInviteLink', {'@type': 'editChatSubscriptionInviteLink', 'chat_id': chat_id, 'invite_link': invite_link, 'name': name})

    async def get_chat_invite_link(self, chat_id: int = None, invite_link: str = None) -> ChatInviteLink:
        """
        description Returns information about an invite link. Requires administrator privileges and can_invite_users right in the chat to get own links and owner privileges to get other links
        chat_id Chat identifier
        invite_link Invite link to get
        """
        return await self._client.call_method('getChatInviteLink', {'@type': 'getChatInviteLink', 'chat_id': chat_id, 'invite_link': invite_link})

    async def get_chat_invite_link_counts(self, chat_id: int = None) -> ChatInviteLinkCounts:
        """
        description Returns the list of chat administrators with number of their invite links. Requires owner privileges in the chat @chat_id Chat identifier
        """
        return await self._client.call_method('getChatInviteLinkCounts', {'@type': 'getChatInviteLinkCounts', 'chat_id': chat_id})

    async def get_chat_invite_links(self, chat_id: int = None, creator_user_id: int = None, is_revoked: bool = None, offset_date: int = None, offset_invite_link: str = None, limit: int = None) -> ChatInviteLinks:
        """
        description Returns invite links for a chat created by specified administrator. Requires administrator privileges and can_invite_users right in the chat to get own links and owner privileges to get other links
        chat_id Chat identifier
        creator_user_id User identifier of a chat administrator. Must be an identifier of the current user for non-owner
        is_revoked Pass true if revoked links need to be returned instead of active or expired
        offset_date Creation date of an invite link starting after which to return invite links; use 0 to get results from the beginning
        offset_invite_link Invite link starting after which to return invite links; use empty string to get results from the beginning
        limit The maximum number of invite links to return; up to 100
        """
        return await self._client.call_method('getChatInviteLinks', {'@type': 'getChatInviteLinks', 'chat_id': chat_id, 'creator_user_id': creator_user_id, 'is_revoked': is_revoked, 'offset_date': offset_date, 'offset_invite_link': offset_invite_link, 'limit': limit})

    async def get_chat_invite_link_members(self, chat_id: int = None, invite_link: str = None, only_with_expired_subscription: bool = None, offset_member: chatInviteLinkMember = None, limit: int = None) -> ChatInviteLinkMembers:
        """
        description Returns chat members joined a chat via an invite link. Requires administrator privileges and can_invite_users right in the chat for own links and owner privileges for other links
        chat_id Chat identifier
        invite_link Invite link for which to return chat members
        only_with_expired_subscription Pass true if the link is a subscription link and only members with expired subscription must be returned
        offset_member A chat member from which to return next chat members; pass null to get results from the beginning
        limit The maximum number of chat members to return; up to 100
        """
        return await self._client.call_method('getChatInviteLinkMembers', {'@type': 'getChatInviteLinkMembers', 'chat_id': chat_id, 'invite_link': invite_link, 'only_with_expired_subscription': only_with_expired_subscription, 'offset_member': offset_member, 'limit': limit})

    async def revoke_chat_invite_link(self, chat_id: int = None, invite_link: str = None) -> ChatInviteLinks:
        """
        description Revokes invite link for a chat. Available for basic groups, supergroups, and channels. Requires administrator privileges and can_invite_users right in the chat for own links and owner privileges for other links.
        chat_id Chat identifier
        invite_link Invite link to be revoked
        """
        return await self._client.call_method('revokeChatInviteLink', {'@type': 'revokeChatInviteLink', 'chat_id': chat_id, 'invite_link': invite_link})

    async def delete_revoked_chat_invite_link(self, chat_id: int = None, invite_link: str = None) -> Ok:
        """
        description Deletes revoked chat invite links. Requires administrator privileges and can_invite_users right in the chat for own links and owner privileges for other links @chat_id Chat identifier @invite_link Invite link to revoke
        """
        return await self._client.call_method('deleteRevokedChatInviteLink', {'@type': 'deleteRevokedChatInviteLink', 'chat_id': chat_id, 'invite_link': invite_link})

    async def delete_all_revoked_chat_invite_links(self, chat_id: int = None, creator_user_id: int = None) -> Ok:
        """
        description Deletes all revoked chat invite links created by a given chat administrator. Requires administrator privileges and can_invite_users right in the chat for own links and owner privileges for other links
        chat_id Chat identifier
        creator_user_id User identifier of a chat administrator, which links will be deleted. Must be an identifier of the current user for non-owner
        """
        return await self._client.call_method('deleteAllRevokedChatInviteLinks', {'@type': 'deleteAllRevokedChatInviteLinks', 'chat_id': chat_id, 'creator_user_id': creator_user_id})

    async def check_chat_invite_link(self, invite_link: str = None) -> ChatInviteLinkInfo:
        """
        description Checks the validity of an invite link for a chat and returns information about the corresponding chat @invite_link Invite link to be checked
        """
        return await self._client.call_method('checkChatInviteLink', {'@type': 'checkChatInviteLink', 'invite_link': invite_link})

    async def join_chat_by_invite_link(self, invite_link: str = None) -> ChatJoinResult:
        """
        description Uses an invite link to add the current user to the chat if possible @invite_link Invite link to use
        """
        return await self._client.call_method('joinChatByInviteLink', {'@type': 'joinChatByInviteLink', 'invite_link': invite_link})

    async def get_chat_join_requests(self, chat_id: int = None, invite_link: str = None, query: str = None, offset_request: chatJoinRequest = None, limit: int = None) -> ChatJoinRequests:
        """
        description Returns pending join requests in a chat
        chat_id Chat identifier
        invite_link Invite link for which to return join requests. If empty, all join requests will be returned. Requires administrator privileges and can_invite_users right in the chat for own links and owner privileges for other links
        query A query to search for in the first names, last names and usernames of the users to return
        offset_request A chat join request from which to return next requests; pass null to get results from the beginning
        limit The maximum number of requests to join the chat to return
        """
        return await self._client.call_method('getChatJoinRequests', {'@type': 'getChatJoinRequests', 'chat_id': chat_id, 'invite_link': invite_link, 'query': query, 'offset_request': offset_request, 'limit': limit})

    async def process_chat_join_request(self, chat_id: int = None, user_id: int = None, approve: bool = None) -> Ok:
        """
        description Handles a pending join request in a chat @chat_id Chat identifier @user_id Identifier of the user who sent the request @approve Pass true to approve the request; pass false to decline it
        """
        return await self._client.call_method('processChatJoinRequest', {'@type': 'processChatJoinRequest', 'chat_id': chat_id, 'user_id': user_id, 'approve': approve})

    async def process_chat_join_requests(self, chat_id: int = None, invite_link: str = None, approve: bool = None) -> Ok:
        """
        description Handles all pending join requests for a given link in a chat
        chat_id Chat identifier
        invite_link Invite link for which to process join requests. If empty, all join requests will be processed. Requires administrator privileges and can_invite_users right in the chat for own links and owner privileges for other links
        approve Pass true to approve all requests; pass false to decline them
        """
        return await self._client.call_method('processChatJoinRequests', {'@type': 'processChatJoinRequests', 'chat_id': chat_id, 'invite_link': invite_link, 'approve': approve})

    async def approve_suggested_post(self, chat_id: int = None, message_id: int = None, send_date: int = None) -> Ok:
        """
        description Approves a suggested post in a channel direct messages chat
        chat_id Chat identifier of the channel direct messages chat
        message_id Identifier of the message with the suggested post. Use messageProperties.can_be_approved to check whether the suggested post can be approved
        send_date Point in time (Unix timestamp) when the post is expected to be published; pass 0 if the date has already been chosen. If specified,
        """
        return await self._client.call_method('approveSuggestedPost', {'@type': 'approveSuggestedPost', 'chat_id': chat_id, 'message_id': message_id, 'send_date': send_date})

    async def decline_suggested_post(self, chat_id: int = None, message_id: int = None, comment: str = None) -> Ok:
        """
        description Declines a suggested post in a channel direct messages chat
        chat_id Chat identifier of the channel direct messages chat
        message_id Identifier of the message with the suggested post. Use messageProperties.can_be_declined to check whether the suggested post can be declined
        comment Comment for the creator of the suggested post; 0-128 characters
        """
        return await self._client.call_method('declineSuggestedPost', {'@type': 'declineSuggestedPost', 'chat_id': chat_id, 'message_id': message_id, 'comment': comment})

    async def add_offer(self, chat_id: int = None, message_id: int = None, options: messageSendOptions = None) -> Message:
        """
        description Sends a suggested post based on a previously sent message in a channel direct messages chat. Can be also used to suggest price or time change for an existing suggested post.
        chat_id Identifier of the channel direct messages chat
        message_id Identifier of the message in the chat which will be sent as suggested post. Use messageProperties.can_add_offer to check whether an offer can be added
        options Options to be used to send the message. New information about the suggested post must always be specified
        """
        return await self._client.call_method('addOffer', {'@type': 'addOffer', 'chat_id': chat_id, 'message_id': message_id, 'options': options})

    async def create_call(self, user_id: int = None, protocol: callProtocol = None, is_video: bool = None) -> CallId:
        """
        description Creates a new call
        user_id Identifier of the user to be called
        protocol The call protocols supported by the application
        is_video Pass true to create a video call
        """
        return await self._client.call_method('createCall', {'@type': 'createCall', 'user_id': user_id, 'protocol': protocol, 'is_video': is_video})

    async def accept_call(self, call_id: int = None, protocol: callProtocol = None) -> Ok:
        """
        description Accepts an incoming call @call_id Call identifier @protocol The call protocols supported by the application
        """
        return await self._client.call_method('acceptCall', {'@type': 'acceptCall', 'call_id': call_id, 'protocol': protocol})

    async def send_call_signaling_data(self, call_id: int = None, data: bytes = None) -> Ok:
        """
        description Sends call signaling data @call_id Call identifier @data The data
        """
        return await self._client.call_method('sendCallSignalingData', {'@type': 'sendCallSignalingData', 'call_id': call_id, 'data': data})

    async def discard_call(self, call_id: int = None, is_disconnected: bool = None, invite_link: str = None, duration: int = None, is_video: bool = None, connection_id: int = None) -> Ok:
        """
        description Discards a call
        call_id Call identifier
        is_disconnected Pass true if the user was disconnected
        invite_link If the call was upgraded to a group call, pass invite link to the group call
        duration The call duration, in seconds
        is_video Pass true if the call was a video call
        connection_id Identifier of the connection used during the call
        """
        return await self._client.call_method('discardCall', {'@type': 'discardCall', 'call_id': call_id, 'is_disconnected': is_disconnected, 'invite_link': invite_link, 'duration': duration, 'is_video': is_video, 'connection_id': connection_id})

    async def send_call_rating(self, call_id: InputCall = None, rating: int = None, comment: str = None, problems: List[CallProblem] = None) -> Ok:
        """
        description Sends a call rating
        call_id Call identifier
        rating Call rating; 1-5
        comment An optional user comment if the rating is less than 5
        problems List of the exact types of problems with the call, specified by the user
        """
        return await self._client.call_method('sendCallRating', {'@type': 'sendCallRating', 'call_id': call_id, 'rating': rating, 'comment': comment, 'problems': problems})

    async def send_call_debug_information(self, call_id: InputCall = None, debug_information: str = None) -> Ok:
        """
        description Sends debug information for a call to Telegram servers @call_id Call identifier @debug_information Debug information in application-specific format
        """
        return await self._client.call_method('sendCallDebugInformation', {'@type': 'sendCallDebugInformation', 'call_id': call_id, 'debug_information': debug_information})

    async def send_call_log(self, call_id: InputCall = None, log_file: InputFile = None) -> Ok:
        """
        description Sends log file for a call to Telegram servers @call_id Call identifier @log_file Call log file. Only inputFileLocal and inputFileGenerated are supported
        """
        return await self._client.call_method('sendCallLog', {'@type': 'sendCallLog', 'call_id': call_id, 'log_file': log_file})

    async def get_video_chat_available_participants(self, chat_id: int = None) -> MessageSenders:
        """
        description Returns the list of participant identifiers, on whose behalf a video chat in the chat can be joined @chat_id Chat identifier
        """
        return await self._client.call_method('getVideoChatAvailableParticipants', {'@type': 'getVideoChatAvailableParticipants', 'chat_id': chat_id})

    async def set_video_chat_default_participant(self, chat_id: int = None, default_participant_id: MessageSender = None) -> Ok:
        """
        description Changes default participant identifier, on whose behalf a video chat in the chat will be joined
        chat_id Chat identifier
        default_participant_id Default group call participant identifier to join the video chats in the chat
        """
        return await self._client.call_method('setVideoChatDefaultParticipant', {'@type': 'setVideoChatDefaultParticipant', 'chat_id': chat_id, 'default_participant_id': default_participant_id})

    async def create_video_chat(self, chat_id: int = None, title: str = None, start_date: int = None, is_rtmp_stream: bool = None) -> GroupCallId:
        """
        description Creates a video chat (a group call bound to a chat); for basic groups, supergroups and channels only; requires can_manage_video_chats administrator right
        chat_id Identifier of a chat in which the video chat will be created
        title Group call title; if empty, chat title will be used
        start_date Point in time (Unix timestamp) when the group call is expected to be started by an administrator; 0 to start the video chat immediately. The date must be at least 10 seconds and at most 8 days in the future
        is_rtmp_stream Pass true to create an RTMP stream instead of an ordinary video chat
        """
        return await self._client.call_method('createVideoChat', {'@type': 'createVideoChat', 'chat_id': chat_id, 'title': title, 'start_date': start_date, 'is_rtmp_stream': is_rtmp_stream})

    async def create_group_call(self, join_parameters: groupCallJoinParameters = None) -> GroupCallInfo:
        """
        description Creates a new group call that isn't bound to a chat @join_parameters Parameters to join the call; pass null to only create call link without joining the call
        """
        return await self._client.call_method('createGroupCall', {'@type': 'createGroupCall', 'join_parameters': join_parameters})

    async def get_video_chat_rtmp_url(self, chat_id: int = None) -> RtmpUrl:
        """
        description Returns RTMP URL for streaming to the video chat of a chat; requires can_manage_video_chats administrator right @chat_id Chat identifier
        """
        return await self._client.call_method('getVideoChatRtmpUrl', {'@type': 'getVideoChatRtmpUrl', 'chat_id': chat_id})

    async def replace_video_chat_rtmp_url(self, chat_id: int = None) -> RtmpUrl:
        """
        description Replaces the current RTMP URL for streaming to the video chat of a chat; requires owner privileges in the chat @chat_id Chat identifier
        """
        return await self._client.call_method('replaceVideoChatRtmpUrl', {'@type': 'replaceVideoChatRtmpUrl', 'chat_id': chat_id})

    async def get_live_story_rtmp_url(self, chat_id: int = None) -> RtmpUrl:
        """
        description Returns RTMP URL for streaming to a live story; requires can_post_stories administrator right for channel chats @chat_id Chat identifier
        """
        return await self._client.call_method('getLiveStoryRtmpUrl', {'@type': 'getLiveStoryRtmpUrl', 'chat_id': chat_id})

    async def replace_live_story_rtmp_url(self, chat_id: int = None) -> RtmpUrl:
        """
        description Replaces the current RTMP URL for streaming to a live story; requires owner privileges for channel chats @chat_id Chat identifier
        """
        return await self._client.call_method('replaceLiveStoryRtmpUrl', {'@type': 'replaceLiveStoryRtmpUrl', 'chat_id': chat_id})

    async def get_group_call(self, group_call_id: int = None) -> GroupCall:
        """
        description Returns information about a group call @group_call_id Group call identifier
        """
        return await self._client.call_method('getGroupCall', {'@type': 'getGroupCall', 'group_call_id': group_call_id})

    async def start_scheduled_video_chat(self, group_call_id: int = None) -> Ok:
        """
        description Starts a scheduled video chat @group_call_id Group call identifier of the video chat
        """
        return await self._client.call_method('startScheduledVideoChat', {'@type': 'startScheduledVideoChat', 'group_call_id': group_call_id})

    async def toggle_video_chat_enabled_start_notification(self, group_call_id: int = None, enabled_start_notification: bool = None) -> Ok:
        """
        description Toggles whether the current user will receive a notification when the video chat starts; for scheduled video chats only
        group_call_id Group call identifier
        enabled_start_notification New value of the enabled_start_notification setting
        """
        return await self._client.call_method('toggleVideoChatEnabledStartNotification', {'@type': 'toggleVideoChatEnabledStartNotification', 'group_call_id': group_call_id, 'enabled_start_notification': enabled_start_notification})

    async def join_group_call(self, input_group_call: InputGroupCall = None, join_parameters: groupCallJoinParameters = None) -> GroupCallInfo:
        """
        description Joins a regular group call that is not bound to a chat @input_group_call The group call to join @join_parameters Parameters to join the call
        """
        return await self._client.call_method('joinGroupCall', {'@type': 'joinGroupCall', 'input_group_call': input_group_call, 'join_parameters': join_parameters})

    async def join_video_chat(self, group_call_id: int = None, participant_id: MessageSender = None, join_parameters: groupCallJoinParameters = None, invite_hash: str = None) -> Text:
        """
        description Joins an active video chat. Returns join response payload for tgcalls
        group_call_id Group call identifier
        participant_id Identifier of a group call participant, which will be used to join the call; pass null to join as self
        join_parameters Parameters to join the call
        invite_hash Invite hash as received from internalLinkTypeVideoChat
        """
        return await self._client.call_method('joinVideoChat', {'@type': 'joinVideoChat', 'group_call_id': group_call_id, 'participant_id': participant_id, 'join_parameters': join_parameters, 'invite_hash': invite_hash})

    async def join_live_story(self, group_call_id: int = None, join_parameters: groupCallJoinParameters = None) -> Text:
        """
        description Joins a group call of an active live story. Returns join response payload for tgcalls
        group_call_id Group call identifier
        join_parameters Parameters to join the call
        """
        return await self._client.call_method('joinLiveStory', {'@type': 'joinLiveStory', 'group_call_id': group_call_id, 'join_parameters': join_parameters})

    async def start_group_call_screen_sharing(self, group_call_id: int = None, audio_source_id: int = None, payload: str = None) -> Text:
        """
        description Starts screen sharing in a joined group call; not supported in live stories. Returns join response payload for tgcalls
        group_call_id Group call identifier
        audio_source_id Screen sharing audio channel synchronization source identifier; received from tgcalls
        payload Group call join payload; received from tgcalls
        """
        return await self._client.call_method('startGroupCallScreenSharing', {'@type': 'startGroupCallScreenSharing', 'group_call_id': group_call_id, 'audio_source_id': audio_source_id, 'payload': payload})

    async def toggle_group_call_screen_sharing_is_paused(self, group_call_id: int = None, is_paused: bool = None) -> Ok:
        """
        description Pauses or unpauses screen sharing in a joined group call; not supported in live stories @group_call_id Group call identifier @is_paused Pass true to pause screen sharing; pass false to unpause it
        """
        return await self._client.call_method('toggleGroupCallScreenSharingIsPaused', {'@type': 'toggleGroupCallScreenSharingIsPaused', 'group_call_id': group_call_id, 'is_paused': is_paused})

    async def end_group_call_screen_sharing(self, group_call_id: int = None) -> Ok:
        """
        description Ends screen sharing in a joined group call; not supported in live stories @group_call_id Group call identifier
        """
        return await self._client.call_method('endGroupCallScreenSharing', {'@type': 'endGroupCallScreenSharing', 'group_call_id': group_call_id})

    async def set_video_chat_title(self, group_call_id: int = None, title: str = None) -> Ok:
        """
        description Sets title of a video chat; requires groupCall.can_be_managed right @group_call_id Group call identifier @title New group call title; 1-64 characters
        """
        return await self._client.call_method('setVideoChatTitle', {'@type': 'setVideoChatTitle', 'group_call_id': group_call_id, 'title': title})

    async def toggle_video_chat_mute_new_participants(self, group_call_id: int = None, mute_new_participants: bool = None) -> Ok:
        """
        description Toggles whether new participants of a video chat can be unmuted only by administrators of the video chat. Requires groupCall.can_toggle_mute_new_participants right
        group_call_id Group call identifier
        mute_new_participants New value of the mute_new_participants setting
        """
        return await self._client.call_method('toggleVideoChatMuteNewParticipants', {'@type': 'toggleVideoChatMuteNewParticipants', 'group_call_id': group_call_id, 'mute_new_participants': mute_new_participants})

    async def toggle_group_call_are_messages_allowed(self, group_call_id: int = None, are_messages_allowed: bool = None) -> Ok:
        """
        description Toggles whether participants of a group call can send messages there. Requires groupCall.can_toggle_are_messages_allowed right
        group_call_id Group call identifier
        are_messages_allowed New value of the are_messages_allowed setting
        """
        return await self._client.call_method('toggleGroupCallAreMessagesAllowed', {'@type': 'toggleGroupCallAreMessagesAllowed', 'group_call_id': group_call_id, 'are_messages_allowed': are_messages_allowed})

    async def get_live_story_streamer(self, group_call_id: int = None) -> GroupCallParticipant:
        """
        description Returns information about the user or the chat that streams to a live story; for live stories that aren't an RTMP stream only @group_call_id Group call identifier
        """
        return await self._client.call_method('getLiveStoryStreamer', {'@type': 'getLiveStoryStreamer', 'group_call_id': group_call_id})

    async def get_live_story_available_message_senders(self, group_call_id: int = None) -> ChatMessageSenders:
        """
        description Returns the list of message sender identifiers, on whose behalf messages can be sent to a live story @group_call_id Group call identifier
        """
        return await self._client.call_method('getLiveStoryAvailableMessageSenders', {'@type': 'getLiveStoryAvailableMessageSenders', 'group_call_id': group_call_id})

    async def set_live_story_message_sender(self, group_call_id: int = None, message_sender_id: MessageSender = None) -> Ok:
        """
        description Selects a message sender to send messages in a live story call
        group_call_id Group call identifier
        message_sender_id New message sender for the group call
        """
        return await self._client.call_method('setLiveStoryMessageSender', {'@type': 'setLiveStoryMessageSender', 'group_call_id': group_call_id, 'message_sender_id': message_sender_id})

    async def send_group_call_message(self, group_call_id: int = None, text: formattedText = None, paid_message_star_count: int = None) -> Ok:
        """
        description Sends a message to other participants of a group call. Requires groupCall.can_send_messages right
        group_call_id Group call identifier
        text Text of the message to send; 1-getOption("group_call_message_text_length_max") characters for non-live-stories; see updateGroupCallMessageLevels for live story restrictions,
        paid_message_star_count The number of Telegram Stars the user agreed to pay to send the message; for live stories only; 0-getOption("paid_group_call_message_star_count_max").
        """
        return await self._client.call_method('sendGroupCallMessage', {'@type': 'sendGroupCallMessage', 'group_call_id': group_call_id, 'text': text, 'paid_message_star_count': paid_message_star_count})

    async def add_pending_live_story_reaction(self, group_call_id: int = None, star_count: int = None) -> Ok:
        """
        description Adds pending paid reaction in a live story group call. Can't be used in live stories posted by the current user.
        group_call_id Group call identifier
        star_count Number of Telegram Stars to be used for the reaction. The total number of pending paid reactions must not exceed getOption("paid_group_call_message_star_count_max")
        """
        return await self._client.call_method('addPendingLiveStoryReaction', {'@type': 'addPendingLiveStoryReaction', 'group_call_id': group_call_id, 'star_count': star_count})

    async def commit_pending_live_story_reactions(self, group_call_id: int = None) -> Ok:
        """
        description Applies all pending paid reactions in a live story group call @group_call_id Group call identifier
        """
        return await self._client.call_method('commitPendingLiveStoryReactions', {'@type': 'commitPendingLiveStoryReactions', 'group_call_id': group_call_id})

    async def remove_pending_live_story_reactions(self, group_call_id: int = None) -> Ok:
        """
        description Removes all pending paid reactions in a live story group call @group_call_id Group call identifier
        """
        return await self._client.call_method('removePendingLiveStoryReactions', {'@type': 'removePendingLiveStoryReactions', 'group_call_id': group_call_id})

    async def delete_group_call_messages(self, group_call_id: int = None, message_ids: List[int] = None, report_spam: bool = None) -> Ok:
        """
        description Deletes messages in a group call; for live story calls only. Requires groupCallMessage.can_be_deleted right
        group_call_id Group call identifier
        message_ids Identifiers of the messages to be deleted
        report_spam Pass true to report the messages as spam
        """
        return await self._client.call_method('deleteGroupCallMessages', {'@type': 'deleteGroupCallMessages', 'group_call_id': group_call_id, 'message_ids': message_ids, 'report_spam': report_spam})

    async def delete_group_call_messages_by_sender(self, group_call_id: int = None, sender_id: MessageSender = None, report_spam: bool = None) -> Ok:
        """
        description Deletes all messages sent by the specified message sender in a group call; for live story calls only. Requires groupCall.can_delete_messages right
        group_call_id Group call identifier
        sender_id Identifier of the sender of messages to delete
        report_spam Pass true to report the messages as spam
        """
        return await self._client.call_method('deleteGroupCallMessagesBySender', {'@type': 'deleteGroupCallMessagesBySender', 'group_call_id': group_call_id, 'sender_id': sender_id, 'report_spam': report_spam})

    async def get_live_story_top_donors(self, group_call_id: int = None) -> LiveStoryDonors:
        """
        description Returns the list of top live story donors @group_call_id Group call identifier of the live story
        """
        return await self._client.call_method('getLiveStoryTopDonors', {'@type': 'getLiveStoryTopDonors', 'group_call_id': group_call_id})

    async def invite_group_call_participant(self, group_call_id: int = None, user_id: int = None, is_video: bool = None) -> InviteGroupCallParticipantResult:
        """
        description Invites a user to an active group call; for group calls not bound to a chat only. Sends a service message of the type messageGroupCall.
        group_call_id Group call identifier
        user_id User identifier
        is_video Pass true if the group call is a video call
        """
        return await self._client.call_method('inviteGroupCallParticipant', {'@type': 'inviteGroupCallParticipant', 'group_call_id': group_call_id, 'user_id': user_id, 'is_video': is_video})

    async def decline_group_call_invitation(self, chat_id: int = None, message_id: int = None) -> Ok:
        """
        description Declines an invitation to an active group call via messageGroupCall. Can be called both by the sender and the receiver of the invitation
        chat_id Identifier of the chat with the message
        message_id Identifier of the message of the type messageGroupCall
        """
        return await self._client.call_method('declineGroupCallInvitation', {'@type': 'declineGroupCallInvitation', 'chat_id': chat_id, 'message_id': message_id})

    async def ban_group_call_participants(self, group_call_id: int = None, user_ids: List[int] = None) -> Ok:
        """
        description Bans users from a group call not bound to a chat; requires groupCall.is_owned. Only the owner of the group call can invite the banned users back
        group_call_id Group call identifier
        user_ids Identifiers of group call participants to ban; identifiers of unknown users from the update updateGroupCallParticipants can be also passed to the method
        """
        return await self._client.call_method('banGroupCallParticipants', {'@type': 'banGroupCallParticipants', 'group_call_id': group_call_id, 'user_ids': user_ids})

    async def invite_video_chat_participants(self, group_call_id: int = None, user_ids: List[int] = None) -> Ok:
        """
        description Invites users to an active video chat. Sends a service message of the type messageInviteVideoChatParticipants to the chat bound to the group call
        group_call_id Group call identifier
        user_ids User identifiers. At most 10 users can be invited simultaneously
        """
        return await self._client.call_method('inviteVideoChatParticipants', {'@type': 'inviteVideoChatParticipants', 'group_call_id': group_call_id, 'user_ids': user_ids})

    async def get_video_chat_invite_link(self, group_call_id: int = None, can_self_unmute: bool = None) -> HttpUrl:
        """
        description Returns invite link to a video chat in a public chat
        group_call_id Group call identifier
        can_self_unmute Pass true if the invite link needs to contain an invite hash, passing which to joinVideoChat would allow the invited user to unmute themselves. Requires groupCall.can_be_managed right
        """
        return await self._client.call_method('getVideoChatInviteLink', {'@type': 'getVideoChatInviteLink', 'group_call_id': group_call_id, 'can_self_unmute': can_self_unmute})

    async def revoke_group_call_invite_link(self, group_call_id: int = None) -> Ok:
        """
        description Revokes invite link for a group call. Requires groupCall.can_be_managed right for video chats or groupCall.is_owned otherwise @group_call_id Group call identifier
        """
        return await self._client.call_method('revokeGroupCallInviteLink', {'@type': 'revokeGroupCallInviteLink', 'group_call_id': group_call_id})

    async def start_group_call_recording(self, group_call_id: int = None, title: str = None, record_video: bool = None, use_portrait_orientation: bool = None) -> Ok:
        """
        description Starts recording of an active group call; for video chats only. Requires groupCall.can_be_managed right
        group_call_id Group call identifier
        title Group call recording title; 0-64 characters
        record_video Pass true to record a video file instead of an audio file
        use_portrait_orientation Pass true to use portrait orientation for video instead of landscape one
        """
        return await self._client.call_method('startGroupCallRecording', {'@type': 'startGroupCallRecording', 'group_call_id': group_call_id, 'title': title, 'record_video': record_video, 'use_portrait_orientation': use_portrait_orientation})

    async def end_group_call_recording(self, group_call_id: int = None) -> Ok:
        """
        description Ends recording of an active group call; for video chats only. Requires groupCall.can_be_managed right @group_call_id Group call identifier
        """
        return await self._client.call_method('endGroupCallRecording', {'@type': 'endGroupCallRecording', 'group_call_id': group_call_id})

    async def toggle_group_call_is_my_video_paused(self, group_call_id: int = None, is_my_video_paused: bool = None) -> Ok:
        """
        description Toggles whether current user's video is paused @group_call_id Group call identifier @is_my_video_paused Pass true if the current user's video is paused
        """
        return await self._client.call_method('toggleGroupCallIsMyVideoPaused', {'@type': 'toggleGroupCallIsMyVideoPaused', 'group_call_id': group_call_id, 'is_my_video_paused': is_my_video_paused})

    async def toggle_group_call_is_my_video_enabled(self, group_call_id: int = None, is_my_video_enabled: bool = None) -> Ok:
        """
        description Toggles whether current user's video is enabled @group_call_id Group call identifier @is_my_video_enabled Pass true if the current user's video is enabled
        """
        return await self._client.call_method('toggleGroupCallIsMyVideoEnabled', {'@type': 'toggleGroupCallIsMyVideoEnabled', 'group_call_id': group_call_id, 'is_my_video_enabled': is_my_video_enabled})

    async def set_group_call_paid_message_star_count(self, group_call_id: int = None, paid_message_star_count: int = None) -> Ok:
        """
        description Changes the minimum number of Telegram Stars that must be paid by general participant for each sent message to a live story call. Requires groupCall.can_be_managed right
        group_call_id Group call identifier; must be an identifier of a live story call
        paid_message_star_count The new minimum number of Telegram Stars; 0-getOption("paid_group_call_message_star_count_max")
        """
        return await self._client.call_method('setGroupCallPaidMessageStarCount', {'@type': 'setGroupCallPaidMessageStarCount', 'group_call_id': group_call_id, 'paid_message_star_count': paid_message_star_count})

    async def set_group_call_participant_is_speaking(self, group_call_id: int = None, audio_source: int = None, is_speaking: bool = None) -> MessageSender:
        """
        description Informs TDLib that speaking state of a participant of an active group call has changed. Returns identifier of the participant if it is found
        group_call_id Group call identifier
        audio_source Group call participant's synchronization audio source identifier, or 0 for the current user
        is_speaking Pass true if the user is speaking
        """
        return await self._client.call_method('setGroupCallParticipantIsSpeaking', {'@type': 'setGroupCallParticipantIsSpeaking', 'group_call_id': group_call_id, 'audio_source': audio_source, 'is_speaking': is_speaking})

    async def toggle_group_call_participant_is_muted(self, group_call_id: int = None, participant_id: MessageSender = None, is_muted: bool = None) -> Ok:
        """
        description Toggles whether a participant of an active group call is muted, unmuted, or allowed to unmute themselves; not supported for live stories
        group_call_id Group call identifier
        participant_id Participant identifier
        is_muted Pass true to mute the user; pass false to unmute them
        """
        return await self._client.call_method('toggleGroupCallParticipantIsMuted', {'@type': 'toggleGroupCallParticipantIsMuted', 'group_call_id': group_call_id, 'participant_id': participant_id, 'is_muted': is_muted})

    async def set_group_call_participant_volume_level(self, group_call_id: int = None, participant_id: MessageSender = None, volume_level: int = None) -> Ok:
        """
        description Changes volume level of a participant of an active group call; not supported for live stories. If the current user can manage the group call or is the owner of the group call,
        group_call_id Group call identifier
        participant_id Participant identifier
        volume_level New participant's volume level; 1-20000 in hundreds of percents
        """
        return await self._client.call_method('setGroupCallParticipantVolumeLevel', {'@type': 'setGroupCallParticipantVolumeLevel', 'group_call_id': group_call_id, 'participant_id': participant_id, 'volume_level': volume_level})

    async def toggle_group_call_participant_is_hand_raised(self, group_call_id: int = None, participant_id: MessageSender = None, is_hand_raised: bool = None) -> Ok:
        """
        description Toggles whether a group call participant hand is rased; for video chats only
        group_call_id Group call identifier
        participant_id Participant identifier
        is_hand_raised Pass true if the user's hand needs to be raised. Only self hand can be raised. Requires groupCall.can_be_managed right to lower other's hand
        """
        return await self._client.call_method('toggleGroupCallParticipantIsHandRaised', {'@type': 'toggleGroupCallParticipantIsHandRaised', 'group_call_id': group_call_id, 'participant_id': participant_id, 'is_hand_raised': is_hand_raised})

    async def get_group_call_participants(self, input_group_call: InputGroupCall = None, limit: int = None) -> GroupCallParticipants:
        """
        description Returns information about participants of a non-joined group call that is not bound to a chat
        input_group_call The group call which participants will be returned
        limit The maximum number of participants to return; must be positive
        """
        return await self._client.call_method('getGroupCallParticipants', {'@type': 'getGroupCallParticipants', 'input_group_call': input_group_call, 'limit': limit})

    async def load_group_call_participants(self, group_call_id: int = None, limit: int = None) -> Ok:
        """
        description Loads more participants of a group call; not supported in live stories. The loaded participants will be received through updates.
        group_call_id Group call identifier. The group call must be previously received through getGroupCall and must be joined or being joined
        limit The maximum number of participants to load; up to 100
        """
        return await self._client.call_method('loadGroupCallParticipants', {'@type': 'loadGroupCallParticipants', 'group_call_id': group_call_id, 'limit': limit})

    async def leave_group_call(self, group_call_id: int = None) -> Ok:
        """
        description Leaves a group call @group_call_id Group call identifier
        """
        return await self._client.call_method('leaveGroupCall', {'@type': 'leaveGroupCall', 'group_call_id': group_call_id})

    async def end_group_call(self, group_call_id: int = None) -> Ok:
        """
        description Ends a group call. Requires groupCall.can_be_managed right for video chats and live stories or groupCall.is_owned otherwise @group_call_id Group call identifier
        """
        return await self._client.call_method('endGroupCall', {'@type': 'endGroupCall', 'group_call_id': group_call_id})

    async def get_group_call_streams(self, group_call_id: int = None) -> GroupCallStreams:
        """
        description Returns information about available streams in a video chat or a live story @group_call_id Group call identifier
        """
        return await self._client.call_method('getGroupCallStreams', {'@type': 'getGroupCallStreams', 'group_call_id': group_call_id})

    async def get_group_call_stream_segment(self, group_call_id: int = None, time_offset: int = None, scale: int = None, channel_id: int = None, video_quality: GroupCallVideoQuality = None) -> Data:
        """
        description Returns a file with a segment of a video chat or live story in a modified OGG format for audio or MPEG-4 format for video
        group_call_id Group call identifier
        time_offset Point in time when the stream segment begins; Unix timestamp in milliseconds
        scale Segment duration scale; 0-1. Segment's duration is 1000/(2**scale) milliseconds
        channel_id Identifier of an audio/video channel to get as received from tgcalls
        video_quality Video quality as received from tgcalls; pass null to get the worst available quality
        """
        return await self._client.call_method('getGroupCallStreamSegment', {'@type': 'getGroupCallStreamSegment', 'group_call_id': group_call_id, 'time_offset': time_offset, 'scale': scale, 'channel_id': channel_id, 'video_quality': video_quality})

    async def encrypt_group_call_data(self, group_call_id: int = None, data_channel: GroupCallDataChannel = None, data: bytes = None, unencrypted_prefix_size: int = None) -> Data:
        """
        description Encrypts group call data before sending them over network using tgcalls
        group_call_id Group call identifier. The call must not be a video chat
        data_channel Data channel for which data is encrypted
        data Data to encrypt
        unencrypted_prefix_size Size of data prefix that must be kept unencrypted
        """
        return await self._client.call_method('encryptGroupCallData', {'@type': 'encryptGroupCallData', 'group_call_id': group_call_id, 'data_channel': data_channel, 'data': data, 'unencrypted_prefix_size': unencrypted_prefix_size})

    async def decrypt_group_call_data(self, group_call_id: int = None, participant_id: MessageSender = None, data_channel: GroupCallDataChannel = None, data: bytes = None) -> Data:
        """
        description Decrypts group call data received by tgcalls
        group_call_id Group call identifier. The call must not be a video chat
        participant_id Identifier of the group call participant, which sent the data
        data_channel Data channel for which data was encrypted; pass null if unknown
        data Data to decrypt
        """
        return await self._client.call_method('decryptGroupCallData', {'@type': 'decryptGroupCallData', 'group_call_id': group_call_id, 'participant_id': participant_id, 'data_channel': data_channel, 'data': data})

    async def set_message_sender_block_list(self, sender_id: MessageSender = None, block_list: BlockList = None) -> Ok:
        """
        description Changes the block list of a message sender. Currently, only users and supergroup chats can be blocked
        sender_id Identifier of a message sender to block/unblock
        block_list New block list for the message sender; pass null to unblock the message sender
        """
        return await self._client.call_method('setMessageSenderBlockList', {'@type': 'setMessageSenderBlockList', 'sender_id': sender_id, 'block_list': block_list})

    async def block_message_sender_from_replies(self, message_id: int = None, delete_message: bool = None, delete_all_messages: bool = None, report_spam: bool = None) -> Ok:
        """
        description Blocks an original sender of a message in the Replies chat
        message_id The identifier of an incoming message in the Replies chat
        delete_message Pass true to delete the message
        delete_all_messages Pass true to delete all messages from the same sender
        report_spam Pass true to report the sender to the Telegram moderators
        """
        return await self._client.call_method('blockMessageSenderFromReplies', {'@type': 'blockMessageSenderFromReplies', 'message_id': message_id, 'delete_message': delete_message, 'delete_all_messages': delete_all_messages, 'report_spam': report_spam})

    async def get_blocked_message_senders(self, block_list: BlockList = None, offset: int = None, limit: int = None) -> MessageSenders:
        """
        description Returns users and chats that were blocked by the current user
        block_list Block list from which to return users
        offset Number of users and chats to skip in the result; must be non-negative
        limit The maximum number of users and chats to return; up to 100
        """
        return await self._client.call_method('getBlockedMessageSenders', {'@type': 'getBlockedMessageSenders', 'block_list': block_list, 'offset': offset, 'limit': limit})

    async def add_contact(self, user_id: int = None, contact: importedContact = None, share_phone_number: bool = None) -> Ok:
        """
        description Adds a user to the contact list or edits an existing contact by their user identifier
        user_id Identifier of the user
        contact The contact to add or edit; phone number may be empty and needs to be specified only if known
        share_phone_number Pass true to share the current user's phone number with the new contact. A corresponding rule to userPrivacySettingShowPhoneNumber will be added if needed.
        """
        return await self._client.call_method('addContact', {'@type': 'addContact', 'user_id': user_id, 'contact': contact, 'share_phone_number': share_phone_number})

    async def import_contacts(self, contacts: List[importedContact] = None) -> ImportedContacts:
        """
        description Adds new contacts or edits existing contacts by their phone numbers; contacts' user identifiers are ignored
        contacts The list of contacts to import or edit
        """
        return await self._client.call_method('importContacts', {'@type': 'importContacts', 'contacts': contacts})

    async def get_contacts(self) -> Users:
        """
        description Returns all contacts of the user
        """
        return await self._client.call_method('getContacts', {'@type': 'getContacts'})

    async def search_contacts(self, query: str = None, limit: int = None) -> Users:
        """
        description Searches for the specified query in the first names, last names and usernames of the known user contacts
        query Query to search for; may be empty to return all contacts
        limit The maximum number of users to be returned
        """
        return await self._client.call_method('searchContacts', {'@type': 'searchContacts', 'query': query, 'limit': limit})

    async def remove_contacts(self, user_ids: List[int] = None) -> Ok:
        """
        description Removes users from the contact list @user_ids Identifiers of users to be deleted
        """
        return await self._client.call_method('removeContacts', {'@type': 'removeContacts', 'user_ids': user_ids})

    async def get_imported_contact_count(self) -> Count:
        """
        description Returns the total number of imported contacts
        """
        return await self._client.call_method('getImportedContactCount', {'@type': 'getImportedContactCount'})

    async def change_imported_contacts(self, contacts: List[importedContact] = None) -> ImportedContacts:
        """
        description Changes imported contacts using the list of contacts saved on the device. Imports newly added contacts and, if at least the file database is enabled, deletes recently deleted contacts.
        contacts The new list of contacts to import
        """
        return await self._client.call_method('changeImportedContacts', {'@type': 'changeImportedContacts', 'contacts': contacts})

    async def clear_imported_contacts(self) -> Ok:
        """
        description Clears all imported contacts, contact list remains unchanged
        """
        return await self._client.call_method('clearImportedContacts', {'@type': 'clearImportedContacts'})

    async def set_close_friends(self, user_ids: List[int] = None) -> Ok:
        """
        description Changes the list of close friends of the current user @user_ids User identifiers of close friends; the users must be contacts of the current user
        """
        return await self._client.call_method('setCloseFriends', {'@type': 'setCloseFriends', 'user_ids': user_ids})

    async def get_close_friends(self) -> Users:
        """
        description Returns all close friends of the current user
        """
        return await self._client.call_method('getCloseFriends', {'@type': 'getCloseFriends'})

    async def set_user_personal_profile_photo(self, user_id: int = None, photo: InputChatPhoto = None) -> Ok:
        """
        description Changes a personal profile photo of a contact user @user_id User identifier @photo Profile photo to set; pass null to delete the photo; inputChatPhotoPrevious isn't supported in this function
        """
        return await self._client.call_method('setUserPersonalProfilePhoto', {'@type': 'setUserPersonalProfilePhoto', 'user_id': user_id, 'photo': photo})

    async def set_user_note(self, user_id: int = None, note: formattedText = None) -> Ok:
        """
        description Changes a note of a contact user
        user_id User identifier
        note Note to set for the user; 0-getOption("user_note_text_length_max") characters. Only Bold, Italic, Underline, Strikethrough, Spoiler, CustomEmoji, and DateTime entities are allowed
        """
        return await self._client.call_method('setUserNote', {'@type': 'setUserNote', 'user_id': user_id, 'note': note})

    async def suggest_user_profile_photo(self, user_id: int = None, photo: InputChatPhoto = None) -> Ok:
        """
        description Suggests a profile photo to another regular user with common messages and allowing non-paid messages
        user_id User identifier
        photo Profile photo to suggest; inputChatPhotoPrevious isn't supported in this function
        """
        return await self._client.call_method('suggestUserProfilePhoto', {'@type': 'suggestUserProfilePhoto', 'user_id': user_id, 'photo': photo})

    async def suggest_user_birthdate(self, user_id: int = None, birthdate: birthdate = None) -> Ok:
        """
        description Suggests a birthdate to another regular user with common messages and allowing non-paid messages
        user_id User identifier
        birthdate Birthdate to suggest
        """
        return await self._client.call_method('suggestUserBirthdate', {'@type': 'suggestUserBirthdate', 'user_id': user_id, 'birthdate': birthdate})

    async def toggle_bot_can_manage_emoji_status(self, bot_user_id: int = None, can_manage_emoji_status: bool = None) -> Ok:
        """
        description Toggles whether the bot can manage emoji status of the current user @bot_user_id User identifier of the bot @can_manage_emoji_status Pass true if the bot is allowed to change emoji status of the user; pass false otherwise
        """
        return await self._client.call_method('toggleBotCanManageEmojiStatus', {'@type': 'toggleBotCanManageEmojiStatus', 'bot_user_id': bot_user_id, 'can_manage_emoji_status': can_manage_emoji_status})

    async def set_user_emoji_status(self, user_id: int = None, emoji_status: emojiStatus = None) -> Ok:
        """
        description Changes the emoji status of a user; for bots only @user_id Identifier of the user @emoji_status New emoji status; pass null to switch to the default badge
        """
        return await self._client.call_method('setUserEmojiStatus', {'@type': 'setUserEmojiStatus', 'user_id': user_id, 'emoji_status': emoji_status})

    async def get_personal_chat_history(self, user_id: int = None, limit: int = None) -> Messages:
        """
        description Returns messages in the personal chat of a given user; for bots only
        user_id User identifier
        limit The maximum number of messages to be returned; 1-20
        """
        return await self._client.call_method('getPersonalChatHistory', {'@type': 'getPersonalChatHistory', 'user_id': user_id, 'limit': limit})

    async def search_user_by_phone_number(self, phone_number: str = None, only_local: bool = None) -> User:
        """
        description Searches a user by their phone number. Returns a 404 error if the user can't be found
        phone_number Phone number to search for
        only_local Pass true to get only locally available information without sending network requests
        """
        return await self._client.call_method('searchUserByPhoneNumber', {'@type': 'searchUserByPhoneNumber', 'phone_number': phone_number, 'only_local': only_local})

    async def share_phone_number(self, user_id: int = None) -> Ok:
        """
        description Shares the phone number of the current user with a mutual contact. Supposed to be called when the user clicks on chatActionBarSharePhoneNumber
        user_id Identifier of the user with whom to share the phone number. The user must be a mutual contact
        """
        return await self._client.call_method('sharePhoneNumber', {'@type': 'sharePhoneNumber', 'user_id': user_id})

    async def get_user_profile_photos(self, user_id: int = None, offset: int = None, limit: int = None) -> ChatPhotos:
        """
        description Returns the profile photos of a user. Personal and public photo aren't returned
        user_id User identifier
        offset The number of photos to skip; must be non-negative
        limit The maximum number of photos to be returned; up to 100
        """
        return await self._client.call_method('getUserProfilePhotos', {'@type': 'getUserProfilePhotos', 'user_id': user_id, 'offset': offset, 'limit': limit})

    async def get_user_profile_audios(self, user_id: int = None, offset: int = None, limit: int = None) -> Audios:
        """
        description Returns the list of profile audio files of a user
        user_id User identifier
        offset The number of audio files to skip; must be non-negative
        limit The maximum number of audio files to be returned; up to 100
        """
        return await self._client.call_method('getUserProfileAudios', {'@type': 'getUserProfileAudios', 'user_id': user_id, 'offset': offset, 'limit': limit})

    async def is_profile_audio(self, file_id: int = None) -> Ok:
        """
        description Checks whether a file is in the profile audio files of the current user. Returns a 404 error if it isn't @file_id Identifier of the audio file to check
        """
        return await self._client.call_method('isProfileAudio', {'@type': 'isProfileAudio', 'file_id': file_id})

    async def add_profile_audio(self, audio: InputFile = None, duration: int = None, title: str = None, performer: str = None) -> Ok:
        """
        description Adds an audio file to the beginning of the profile audio files of the current user
        audio The audio file to be added
        duration Duration of the audio, in seconds; may be replaced by the server; ignored for already uploaded files
        title Title of the audio; 0-64 characters; may be replaced by the server; ignored for already uploaded files
        performer Performer of the audio; 0-64 characters, may be replaced by the server; ignored for already uploaded files
        """
        return await self._client.call_method('addProfileAudio', {'@type': 'addProfileAudio', 'audio': audio, 'duration': duration, 'title': title, 'performer': performer})

    async def set_profile_audio_position(self, file_id: int = None, after_file_id: int = None) -> Ok:
        """
        description Changes position of an audio file in the profile audio files of the current user
        file_id Identifier of the file from profile audio files, which position will be changed
        after_file_id Identifier of the file from profile audio files after which the file will be positioned; pass 0 to move the file to the beginning of the list
        """
        return await self._client.call_method('setProfileAudioPosition', {'@type': 'setProfileAudioPosition', 'file_id': file_id, 'after_file_id': after_file_id})

    async def remove_profile_audio(self, file_id: int = None) -> Ok:
        """
        description Removes an audio file from the profile audio files of the current user @file_id Identifier of the audio file to be removed
        """
        return await self._client.call_method('removeProfileAudio', {'@type': 'removeProfileAudio', 'file_id': file_id})

    async def get_sticker_outline(self, sticker_file_id: int = None, for_animated_emoji: bool = None, for_clicked_animated_emoji_message: bool = None) -> Outline:
        """
        description Returns outline of a sticker. This is an offline method. Returns a 404 error if the outline isn't known
        sticker_file_id File identifier of the sticker
        for_animated_emoji Pass true to get the outline scaled for animated emoji
        for_clicked_animated_emoji_message Pass true to get the outline scaled for clicked animated emoji message
        """
        return await self._client.call_method('getStickerOutline', {'@type': 'getStickerOutline', 'sticker_file_id': sticker_file_id, 'for_animated_emoji': for_animated_emoji, 'for_clicked_animated_emoji_message': for_clicked_animated_emoji_message})

    async def get_sticker_outline_svg_path(self, sticker_file_id: int = None, for_animated_emoji: bool = None, for_clicked_animated_emoji_message: bool = None) -> Text:
        """
        description Returns outline of a sticker as an SVG path. This is an offline method. Returns an empty string if the outline isn't known
        sticker_file_id File identifier of the sticker
        for_animated_emoji Pass true to get the outline scaled for animated emoji
        for_clicked_animated_emoji_message Pass true to get the outline scaled for clicked animated emoji message
        """
        return await self._client.call_method('getStickerOutlineSvgPath', {'@type': 'getStickerOutlineSvgPath', 'sticker_file_id': sticker_file_id, 'for_animated_emoji': for_animated_emoji, 'for_clicked_animated_emoji_message': for_clicked_animated_emoji_message})

    async def get_stickers(self, sticker_type: StickerType = None, query: str = None, limit: int = None, chat_id: int = None) -> Stickers:
        """
        description Returns stickers from the installed sticker sets that correspond to any of the given emoji or can be found by sticker-specific keywords. If the query is non-empty, then favorite, recently used or trending stickers may also be returned
        sticker_type Type of the stickers to return
        query Search query; a space-separated list of emojis or a keyword prefix. If empty, returns all known installed stickers
        limit The maximum number of stickers to be returned
        chat_id Chat identifier for which to return stickers. Available custom emoji stickers may be different for different chats
        """
        return await self._client.call_method('getStickers', {'@type': 'getStickers', 'sticker_type': sticker_type, 'query': query, 'limit': limit, 'chat_id': chat_id})

    async def get_all_sticker_emojis(self, sticker_type: StickerType = None, query: str = None, chat_id: int = None, return_only_main_emoji: bool = None) -> Emojis:
        """
        description Returns unique emoji that correspond to stickers to be found by the getStickers(sticker_type, query, 1000000, chat_id)
        sticker_type Type of the stickers to search for
        query Search query
        chat_id Chat identifier for which to find stickers
        return_only_main_emoji Pass true if only main emoji for each found sticker must be included in the result
        """
        return await self._client.call_method('getAllStickerEmojis', {'@type': 'getAllStickerEmojis', 'sticker_type': sticker_type, 'query': query, 'chat_id': chat_id, 'return_only_main_emoji': return_only_main_emoji})

    async def search_stickers(self, sticker_type: StickerType = None, emojis: str = None, query: str = None, input_language_codes: List[str] = None, offset: int = None, limit: int = None) -> Stickers:
        """
        description Searches for stickers from public sticker sets that correspond to any of the given emoji
        sticker_type Type of the stickers to return
        emojis Space-separated list of emojis to search for
        query Query to search for; may be empty to search for emoji only
        input_language_codes List of possible IETF language tags of the user's input language; may be empty if unknown
        offset The offset from which to return the stickers; must be non-negative
        limit The maximum number of stickers to be returned; 0-100
        """
        return await self._client.call_method('searchStickers', {'@type': 'searchStickers', 'sticker_type': sticker_type, 'emojis': emojis, 'query': query, 'input_language_codes': input_language_codes, 'offset': offset, 'limit': limit})

    async def get_greeting_stickers(self) -> Stickers:
        """
        description Returns greeting stickers from regular sticker sets that can be used for the start page of other users
        """
        return await self._client.call_method('getGreetingStickers', {'@type': 'getGreetingStickers'})

    async def get_premium_stickers(self, limit: int = None) -> Stickers:
        """
        description Returns premium stickers from regular sticker sets @limit The maximum number of stickers to be returned; 0-100
        """
        return await self._client.call_method('getPremiumStickers', {'@type': 'getPremiumStickers', 'limit': limit})

    async def get_installed_sticker_sets(self, sticker_type: StickerType = None) -> StickerSets:
        """
        description Returns a list of installed sticker sets @sticker_type Type of the sticker sets to return
        """
        return await self._client.call_method('getInstalledStickerSets', {'@type': 'getInstalledStickerSets', 'sticker_type': sticker_type})

    async def get_archived_sticker_sets(self, sticker_type: StickerType = None, offset_sticker_set_id: int = None, limit: int = None) -> StickerSets:
        """
        description Returns a list of archived sticker sets
        sticker_type Type of the sticker sets to return
        offset_sticker_set_id Identifier of the sticker set from which to return the result; use 0 to get results from the beginning
        limit The maximum number of sticker sets to return; up to 100
        """
        return await self._client.call_method('getArchivedStickerSets', {'@type': 'getArchivedStickerSets', 'sticker_type': sticker_type, 'offset_sticker_set_id': offset_sticker_set_id, 'limit': limit})

    async def get_trending_sticker_sets(self, sticker_type: StickerType = None, offset: int = None, limit: int = None) -> TrendingStickerSets:
        """
        description Returns a list of trending sticker sets. For optimal performance, the number of returned sticker sets is chosen by TDLib
        sticker_type Type of the sticker sets to return
        offset The offset from which to return the sticker sets; must be non-negative
        limit The maximum number of sticker sets to be returned; up to 100. For optimal performance, the number of returned sticker sets is chosen by TDLib and can be smaller than the specified limit, even if the end of the list has not been reached
        """
        return await self._client.call_method('getTrendingStickerSets', {'@type': 'getTrendingStickerSets', 'sticker_type': sticker_type, 'offset': offset, 'limit': limit})

    async def get_attached_sticker_sets(self, file_id: int = None) -> StickerSets:
        """
        description Returns a list of sticker sets attached to a file, including regular, mask, and emoji sticker sets. Currently, only animations, photos, and videos can have attached sticker sets @file_id File identifier
        """
        return await self._client.call_method('getAttachedStickerSets', {'@type': 'getAttachedStickerSets', 'file_id': file_id})

    async def get_sticker_set(self, set_id: int = None) -> StickerSet:
        """
        description Returns information about a sticker set by its identifier @set_id Identifier of the sticker set
        """
        return await self._client.call_method('getStickerSet', {'@type': 'getStickerSet', 'set_id': set_id})

    async def get_sticker_set_name(self, set_id: int = None) -> Text:
        """
        description Returns name of a sticker set by its identifier @set_id Identifier of the sticker set
        """
        return await self._client.call_method('getStickerSetName', {'@type': 'getStickerSetName', 'set_id': set_id})

    async def search_sticker_set(self, name: str = None, ignore_cache: bool = None) -> StickerSet:
        """
        description Searches for a sticker set by its name @name Name of the sticker set @ignore_cache Pass true to ignore local cache of sticker sets and always send a network request
        """
        return await self._client.call_method('searchStickerSet', {'@type': 'searchStickerSet', 'name': name, 'ignore_cache': ignore_cache})

    async def search_installed_sticker_sets(self, sticker_type: StickerType = None, query: str = None, limit: int = None) -> StickerSets:
        """
        description Searches for installed sticker sets by looking for specified query in their title and name @sticker_type Type of the sticker sets to search for @query Query to search for @limit The maximum number of sticker sets to return
        """
        return await self._client.call_method('searchInstalledStickerSets', {'@type': 'searchInstalledStickerSets', 'sticker_type': sticker_type, 'query': query, 'limit': limit})

    async def search_sticker_sets(self, sticker_type: StickerType = None, query: str = None) -> StickerSets:
        """
        description Searches for sticker sets by looking for specified query in their title and name. Excludes installed sticker sets from the results
        sticker_type Type of the sticker sets to return
        query Query to search for
        """
        return await self._client.call_method('searchStickerSets', {'@type': 'searchStickerSets', 'sticker_type': sticker_type, 'query': query})

    async def change_sticker_set(self, set_id: int = None, is_installed: bool = None, is_archived: bool = None) -> Ok:
        """
        description Installs/uninstalls or activates/archives a sticker set @set_id Identifier of the sticker set @is_installed The new value of is_installed @is_archived The new value of is_archived. A sticker set can't be installed and archived simultaneously
        """
        return await self._client.call_method('changeStickerSet', {'@type': 'changeStickerSet', 'set_id': set_id, 'is_installed': is_installed, 'is_archived': is_archived})

    async def view_trending_sticker_sets(self, sticker_set_ids: List[int] = None) -> Ok:
        """
        description Informs the server that some trending sticker sets have been viewed by the user @sticker_set_ids Identifiers of viewed trending sticker sets
        """
        return await self._client.call_method('viewTrendingStickerSets', {'@type': 'viewTrendingStickerSets', 'sticker_set_ids': sticker_set_ids})

    async def reorder_installed_sticker_sets(self, sticker_type: StickerType = None, sticker_set_ids: List[int] = None) -> Ok:
        """
        description Changes the order of installed sticker sets @sticker_type Type of the sticker sets to reorder @sticker_set_ids Identifiers of installed sticker sets in the new correct order
        """
        return await self._client.call_method('reorderInstalledStickerSets', {'@type': 'reorderInstalledStickerSets', 'sticker_type': sticker_type, 'sticker_set_ids': sticker_set_ids})

    async def get_recent_stickers(self, is_attached: bool = None) -> Stickers:
        """
        description Returns a list of recently used stickers @is_attached Pass true to return stickers and masks that were recently attached to photos or video files; pass false to return recently sent stickers
        """
        return await self._client.call_method('getRecentStickers', {'@type': 'getRecentStickers', 'is_attached': is_attached})

    async def add_recent_sticker(self, is_attached: bool = None, sticker: InputFile = None) -> Stickers:
        """
        description Manually adds a new sticker to the list of recently used stickers. The new sticker is added to the top of the list. If the sticker was already in the list, it is removed from the list first.
        is_attached Pass true to add the sticker to the list of stickers recently attached to photo or video files; pass false to add the sticker to the list of recently sent stickers
        sticker Sticker file to add
        """
        return await self._client.call_method('addRecentSticker', {'@type': 'addRecentSticker', 'is_attached': is_attached, 'sticker': sticker})

    async def remove_recent_sticker(self, is_attached: bool = None, sticker: InputFile = None) -> Ok:
        """
        description Removes a sticker from the list of recently used stickers @is_attached Pass true to remove the sticker from the list of stickers recently attached to photo or video files; pass false to remove the sticker from the list of recently sent stickers @sticker Sticker file to delete
        """
        return await self._client.call_method('removeRecentSticker', {'@type': 'removeRecentSticker', 'is_attached': is_attached, 'sticker': sticker})

    async def clear_recent_stickers(self, is_attached: bool = None) -> Ok:
        """
        description Clears the list of recently used stickers @is_attached Pass true to clear the list of stickers recently attached to photo or video files; pass false to clear the list of recently sent stickers
        """
        return await self._client.call_method('clearRecentStickers', {'@type': 'clearRecentStickers', 'is_attached': is_attached})

    async def get_favorite_stickers(self) -> Stickers:
        """
        description Returns favorite stickers
        """
        return await self._client.call_method('getFavoriteStickers', {'@type': 'getFavoriteStickers'})

    async def add_favorite_sticker(self, sticker: InputFile = None) -> Ok:
        """
        description Adds a new sticker to the list of favorite stickers. The new sticker is added to the top of the list. If the sticker was already in the list, it is removed from the list first.
        sticker Sticker file to add
        """
        return await self._client.call_method('addFavoriteSticker', {'@type': 'addFavoriteSticker', 'sticker': sticker})

    async def remove_favorite_sticker(self, sticker: InputFile = None) -> Ok:
        """
        description Removes a sticker from the list of favorite stickers @sticker Sticker file to delete from the list
        """
        return await self._client.call_method('removeFavoriteSticker', {'@type': 'removeFavoriteSticker', 'sticker': sticker})

    async def get_sticker_emojis(self, sticker: InputFile = None) -> Emojis:
        """
        description Returns emoji corresponding to a sticker. The list is only for informational purposes, because a sticker is always sent with a fixed emoji from the corresponding Sticker object @sticker Sticker file identifier
        """
        return await self._client.call_method('getStickerEmojis', {'@type': 'getStickerEmojis', 'sticker': sticker})

    async def search_emojis(self, text: str = None, input_language_codes: List[str] = None) -> EmojiKeywords:
        """
        description Searches for emojis by keywords. Supported only if the file database is enabled. Order of results is unspecified
        text Text to search for
        input_language_codes List of possible IETF language tags of the user's input language; may be empty if unknown
        """
        return await self._client.call_method('searchEmojis', {'@type': 'searchEmojis', 'text': text, 'input_language_codes': input_language_codes})

    async def get_keyword_emojis(self, text: str = None, input_language_codes: List[str] = None) -> Emojis:
        """
        description Returns emojis matching the keyword. Supported only if the file database is enabled. Order of results is unspecified
        text Text to search for
        input_language_codes List of possible IETF language tags of the user's input language; may be empty if unknown
        """
        return await self._client.call_method('getKeywordEmojis', {'@type': 'getKeywordEmojis', 'text': text, 'input_language_codes': input_language_codes})

    async def get_emoji_categories(self, type: EmojiCategoryType = None) -> EmojiCategories:
        """
        description Returns available emoji categories @type Type of emoji categories to return; pass null to get default emoji categories
        """
        return await self._client.call_method('getEmojiCategories', {'@type': 'getEmojiCategories', 'type': type})

    async def get_animated_emoji(self, emoji: str = None) -> AnimatedEmoji:
        """
        description Returns an animated emoji corresponding to a given emoji. Returns a 404 error if the emoji has no animated emoji @emoji The emoji
        """
        return await self._client.call_method('getAnimatedEmoji', {'@type': 'getAnimatedEmoji', 'emoji': emoji})

    async def get_emoji_suggestions_url(self, language_code: str = None) -> HttpUrl:
        """
        description Returns an HTTP URL which can be used to automatically log in to the translation platform and suggest new emoji replacements. The URL will be valid for 30 seconds after generation
        language_code Language code for which the emoji replacements will be suggested
        """
        return await self._client.call_method('getEmojiSuggestionsUrl', {'@type': 'getEmojiSuggestionsUrl', 'language_code': language_code})

    async def get_custom_emoji_stickers(self, custom_emoji_ids: List[int] = None) -> Stickers:
        """
        description Returns the list of custom emoji stickers by their identifiers. Stickers are returned in arbitrary order. Only found stickers are returned
        custom_emoji_ids Identifiers of custom emoji stickers. At most 200 custom emoji stickers can be received simultaneously
        """
        return await self._client.call_method('getCustomEmojiStickers', {'@type': 'getCustomEmojiStickers', 'custom_emoji_ids': custom_emoji_ids})

    async def get_default_chat_photo_custom_emoji_stickers(self) -> Stickers:
        """
        description Returns default list of custom emoji stickers for placing on a chat photo
        """
        return await self._client.call_method('getDefaultChatPhotoCustomEmojiStickers', {'@type': 'getDefaultChatPhotoCustomEmojiStickers'})

    async def get_default_profile_photo_custom_emoji_stickers(self) -> Stickers:
        """
        description Returns default list of custom emoji stickers for placing on a profile photo
        """
        return await self._client.call_method('getDefaultProfilePhotoCustomEmojiStickers', {'@type': 'getDefaultProfilePhotoCustomEmojiStickers'})

    async def get_default_background_custom_emoji_stickers(self) -> Stickers:
        """
        description Returns default list of custom emoji stickers for reply background
        """
        return await self._client.call_method('getDefaultBackgroundCustomEmojiStickers', {'@type': 'getDefaultBackgroundCustomEmojiStickers'})

    async def get_saved_animations(self) -> Animations:
        """
        description Returns saved animations
        """
        return await self._client.call_method('getSavedAnimations', {'@type': 'getSavedAnimations'})

    async def add_saved_animation(self, animation: InputFile = None) -> Ok:
        """
        description Manually adds a new animation to the list of saved animations. The new animation is added to the beginning of the list. If the animation was already in the list, it is removed first.
        animation The animation file to be added. Only animations known to the server (i.e., successfully sent via a message) can be added to the list
        """
        return await self._client.call_method('addSavedAnimation', {'@type': 'addSavedAnimation', 'animation': animation})

    async def remove_saved_animation(self, animation: InputFile = None) -> Ok:
        """
        description Removes an animation from the list of saved animations @animation Animation file to be removed
        """
        return await self._client.call_method('removeSavedAnimation', {'@type': 'removeSavedAnimation', 'animation': animation})

    async def get_recent_inline_bots(self) -> Users:
        """
        description Returns up to 20 recently used inline bots in the order of their last usage
        """
        return await self._client.call_method('getRecentInlineBots', {'@type': 'getRecentInlineBots'})

    async def get_owned_bots(self) -> Users:
        """
        description Returns the list of bots owned by the current user
        """
        return await self._client.call_method('getOwnedBots', {'@type': 'getOwnedBots'})

    async def search_hashtags(self, prefix: str = None, limit: int = None) -> Hashtags:
        """
        description Searches for recently used hashtags by their prefix @prefix Hashtag prefix to search for @limit The maximum number of hashtags to be returned
        """
        return await self._client.call_method('searchHashtags', {'@type': 'searchHashtags', 'prefix': prefix, 'limit': limit})

    async def remove_recent_hashtag(self, hashtag: str = None) -> Ok:
        """
        description Removes a hashtag from the list of recently used hashtags @hashtag Hashtag to delete
        """
        return await self._client.call_method('removeRecentHashtag', {'@type': 'removeRecentHashtag', 'hashtag': hashtag})

    async def get_link_preview(self, text: formattedText = None, link_preview_options: linkPreviewOptions = None) -> LinkPreview:
        """
        description Returns a link preview by the text of a message. Do not call this function too often. Returns a 404 error if the text has no link preview
        text Message text with formatting
        link_preview_options Options to be used for generation of the link preview; pass null to use default link preview options
        """
        return await self._client.call_method('getLinkPreview', {'@type': 'getLinkPreview', 'text': text, 'link_preview_options': link_preview_options})

    async def get_web_page_instant_view(self, url: str = None, only_local: bool = None) -> WebPageInstantView:
        """
        description Returns an instant view version of a web page if available. This is an offline method if only_local is true. Returns a 404 error if the web page has no instant view page
        url The web page URL
        only_local Pass true to get only locally available information without sending network requests
        """
        return await self._client.call_method('getWebPageInstantView', {'@type': 'getWebPageInstantView', 'url': url, 'only_local': only_local})

    async def set_profile_photo(self, photo: InputChatPhoto = None, is_public: bool = None) -> Ok:
        """
        description Changes a profile photo for the current user
        photo Profile photo to set
        is_public Pass true to set the public photo, which will be visible even if the main photo is hidden by privacy settings
        """
        return await self._client.call_method('setProfilePhoto', {'@type': 'setProfilePhoto', 'photo': photo, 'is_public': is_public})

    async def delete_profile_photo(self, profile_photo_id: int = None) -> Ok:
        """
        description Deletes a profile photo @profile_photo_id Identifier of the profile photo to delete
        """
        return await self._client.call_method('deleteProfilePhoto', {'@type': 'deleteProfilePhoto', 'profile_photo_id': profile_photo_id})

    async def set_accent_color(self, accent_color_id: int = None, background_custom_emoji_id: int = None) -> Ok:
        """
        description Changes accent color and background custom emoji for the current user; for Telegram Premium users only
        accent_color_id Identifier of the accent color to use
        background_custom_emoji_id Identifier of a custom emoji to be shown on the reply header and link preview background; 0 if none
        """
        return await self._client.call_method('setAccentColor', {'@type': 'setAccentColor', 'accent_color_id': accent_color_id, 'background_custom_emoji_id': background_custom_emoji_id})

    async def set_upgraded_gift_colors(self, upgraded_gift_colors_id: int = None) -> Ok:
        """
        description Changes color scheme for the current user based on an owned or a hosted upgraded gift; for Telegram Premium users only
        upgraded_gift_colors_id Identifier of the upgradedGiftColors scheme to use
        """
        return await self._client.call_method('setUpgradedGiftColors', {'@type': 'setUpgradedGiftColors', 'upgraded_gift_colors_id': upgraded_gift_colors_id})

    async def set_profile_accent_color(self, profile_accent_color_id: int = None, profile_background_custom_emoji_id: int = None) -> Ok:
        """
        description Changes accent color and background custom emoji for profile of the current user; for Telegram Premium users only
        profile_accent_color_id Identifier of the accent color to use for profile; pass -1 if none
        profile_background_custom_emoji_id Identifier of a custom emoji to be shown on the user's profile photo background; 0 if none
        """
        return await self._client.call_method('setProfileAccentColor', {'@type': 'setProfileAccentColor', 'profile_accent_color_id': profile_accent_color_id, 'profile_background_custom_emoji_id': profile_background_custom_emoji_id})

    async def set_name(self, first_name: str = None, last_name: str = None) -> Ok:
        """
        description Changes the first and last name of the current user @first_name The new value of the first name for the current user; 1-64 characters @last_name The new value of the optional last name for the current user; 0-64 characters
        """
        return await self._client.call_method('setName', {'@type': 'setName', 'first_name': first_name, 'last_name': last_name})

    async def set_bio(self, bio: str = None) -> Ok:
        """
        description Changes the bio of the current user @bio The new value of the user bio; 0-getOption("bio_length_max") characters without line feeds
        """
        return await self._client.call_method('setBio', {'@type': 'setBio', 'bio': bio})

    async def set_username(self, username: str = None) -> Ok:
        """
        description Changes the editable username of the current user
        username The new value of the username. Use an empty string to remove the username. The username can't be completely removed if there is another active or disabled username
        """
        return await self._client.call_method('setUsername', {'@type': 'setUsername', 'username': username})

    async def toggle_username_is_active(self, username: str = None, is_active: bool = None) -> Ok:
        """
        description Changes active state for a username of the current user. The editable username can't be disabled. May return an error with a message "USERNAMES_ACTIVE_TOO_MUCH" if the maximum number of active usernames has been reached
        username The username to change
        is_active Pass true to activate the username; pass false to disable it
        """
        return await self._client.call_method('toggleUsernameIsActive', {'@type': 'toggleUsernameIsActive', 'username': username, 'is_active': is_active})

    async def reorder_active_usernames(self, usernames: List[str] = None) -> Ok:
        """
        description Changes order of active usernames of the current user @usernames The new order of active usernames. All currently active usernames must be specified
        """
        return await self._client.call_method('reorderActiveUsernames', {'@type': 'reorderActiveUsernames', 'usernames': usernames})

    async def set_birthdate(self, birthdate: birthdate = None) -> Ok:
        """
        description Changes the birthdate of the current user @birthdate The new value of the current user's birthdate; pass null to remove the birthdate
        """
        return await self._client.call_method('setBirthdate', {'@type': 'setBirthdate', 'birthdate': birthdate})

    async def set_main_profile_tab(self, main_profile_tab: ProfileTab = None) -> Ok:
        """
        description Changes the main profile tab of the current user @main_profile_tab The new value of the main profile tab
        """
        return await self._client.call_method('setMainProfileTab', {'@type': 'setMainProfileTab', 'main_profile_tab': main_profile_tab})

    async def set_personal_chat(self, chat_id: int = None) -> Ok:
        """
        description Changes the personal chat of the current user @chat_id Identifier of the new personal chat; pass 0 to remove the chat. Use getSuitablePersonalChats to get suitable chats
        """
        return await self._client.call_method('setPersonalChat', {'@type': 'setPersonalChat', 'chat_id': chat_id})

    async def set_emoji_status(self, emoji_status: emojiStatus = None) -> Ok:
        """
        description Changes the emoji status of the current user; for Telegram Premium users only @emoji_status New emoji status; pass null to switch to the default badge
        """
        return await self._client.call_method('setEmojiStatus', {'@type': 'setEmojiStatus', 'emoji_status': emoji_status})

    async def toggle_has_sponsored_messages_enabled(self, has_sponsored_messages_enabled: bool = None) -> Ok:
        """
        description Toggles whether the current user has sponsored messages enabled. The setting has no effect for users without Telegram Premium for which sponsored messages are always enabled
        has_sponsored_messages_enabled Pass true to enable sponsored messages for the current user; false to disable them
        """
        return await self._client.call_method('toggleHasSponsoredMessagesEnabled', {'@type': 'toggleHasSponsoredMessagesEnabled', 'has_sponsored_messages_enabled': has_sponsored_messages_enabled})

    async def set_business_location(self, location: businessLocation = None) -> Ok:
        """
        description Changes the business location of the current user. Requires Telegram Business subscription @location The new location of the business; pass null to remove the location
        """
        return await self._client.call_method('setBusinessLocation', {'@type': 'setBusinessLocation', 'location': location})

    async def set_business_opening_hours(self, opening_hours: businessOpeningHours = None) -> Ok:
        """
        description Changes the business opening hours of the current user. Requires Telegram Business subscription
        opening_hours The new opening hours of the business; pass null to remove the opening hours; up to 28 time intervals can be specified
        """
        return await self._client.call_method('setBusinessOpeningHours', {'@type': 'setBusinessOpeningHours', 'opening_hours': opening_hours})

    async def set_business_greeting_message_settings(self, greeting_message_settings: businessGreetingMessageSettings = None) -> Ok:
        """
        description Changes the business greeting message settings of the current user. Requires Telegram Business subscription @greeting_message_settings The new settings for the greeting message of the business; pass null to disable the greeting message
        """
        return await self._client.call_method('setBusinessGreetingMessageSettings', {'@type': 'setBusinessGreetingMessageSettings', 'greeting_message_settings': greeting_message_settings})

    async def set_business_away_message_settings(self, away_message_settings: businessAwayMessageSettings = None) -> Ok:
        """
        description Changes the business away message settings of the current user. Requires Telegram Business subscription @away_message_settings The new settings for the away message of the business; pass null to disable the away message
        """
        return await self._client.call_method('setBusinessAwayMessageSettings', {'@type': 'setBusinessAwayMessageSettings', 'away_message_settings': away_message_settings})

    async def set_business_start_page(self, start_page: inputBusinessStartPage = None) -> Ok:
        """
        description Changes the business start page of the current user. Requires Telegram Business subscription @start_page The new start page of the business; pass null to remove custom start page
        """
        return await self._client.call_method('setBusinessStartPage', {'@type': 'setBusinessStartPage', 'start_page': start_page})

    async def send_phone_number_code(self, phone_number: str = None, settings: phoneNumberAuthenticationSettings = None, type: PhoneNumberCodeType = None) -> AuthenticationCodeInfo:
        """
        description Sends a code to the specified phone number. Aborts previous phone number verification if there was one. On success, returns information about the sent code
        phone_number The phone number, in international format
        settings Settings for the authentication of the user's phone number; pass null to use default settings
        type Type of the request for which the code is sent
        """
        return await self._client.call_method('sendPhoneNumberCode', {'@type': 'sendPhoneNumberCode', 'phone_number': phone_number, 'settings': settings, 'type': type})

    async def send_phone_number_firebase_sms(self, token: str = None) -> Ok:
        """
        description Sends Firebase Authentication SMS to the specified phone number. Works only when received a code of the type authenticationCodeTypeFirebaseAndroid or authenticationCodeTypeFirebaseIos
        token Play Integrity API or SafetyNet Attestation API token for the Android application, or secret from push notification for the iOS application
        """
        return await self._client.call_method('sendPhoneNumberFirebaseSms', {'@type': 'sendPhoneNumberFirebaseSms', 'token': token})

    async def report_phone_number_code_missing(self, mobile_network_code: str = None) -> Ok:
        """
        description Reports that authentication code wasn't delivered via SMS to the specified phone number; for official mobile applications only @mobile_network_code Current mobile network code
        """
        return await self._client.call_method('reportPhoneNumberCodeMissing', {'@type': 'reportPhoneNumberCodeMissing', 'mobile_network_code': mobile_network_code})

    async def resend_phone_number_code(self, reason: ResendCodeReason = None) -> AuthenticationCodeInfo:
        """
        description Resends the authentication code sent to a phone number. Works only if the previously received authenticationCodeInfo next_code_type was not null and the server-specified timeout has passed
        reason Reason of code resending; pass null if unknown
        """
        return await self._client.call_method('resendPhoneNumberCode', {'@type': 'resendPhoneNumberCode', 'reason': reason})

    async def check_phone_number_code(self, code: str = None) -> Ok:
        """
        description Checks the authentication code and completes the request for which the code was sent if appropriate @code Authentication code to check
        """
        return await self._client.call_method('checkPhoneNumberCode', {'@type': 'checkPhoneNumberCode', 'code': code})

    async def get_business_connected_bot(self) -> BusinessConnectedBotInfo:
        """
        description Returns information about the business bot that is connected to the current user account. Returns a 404 error if there is no connected bot
        """
        return await self._client.call_method('getBusinessConnectedBot', {'@type': 'getBusinessConnectedBot'})

    async def set_business_connected_bot(self, bot: businessConnectedBot = None) -> Ok:
        """
        description Adds or changes business bot that is connected to the current user account @bot Connection settings for the bot
        """
        return await self._client.call_method('setBusinessConnectedBot', {'@type': 'setBusinessConnectedBot', 'bot': bot})

    async def confirm_business_connected_bot(self, bot_user_id: int = None) -> Ok:
        """
        description Confirms an unconfirmed business connection of the current user from another device @bot_user_id User identifier of the bot
        """
        return await self._client.call_method('confirmBusinessConnectedBot', {'@type': 'confirmBusinessConnectedBot', 'bot_user_id': bot_user_id})

    async def delete_business_connected_bot(self, bot_user_id: int = None) -> Ok:
        """
        description Deletes the business bot that is connected to the current user account @bot_user_id Unique user identifier for the bot
        """
        return await self._client.call_method('deleteBusinessConnectedBot', {'@type': 'deleteBusinessConnectedBot', 'bot_user_id': bot_user_id})

    async def toggle_business_connected_bot_chat_is_paused(self, chat_id: int = None, is_paused: bool = None) -> Ok:
        """
        description Pauses or resumes the connected business bot in a specific chat @chat_id Chat identifier @is_paused Pass true to pause the connected bot in the chat; pass false to resume the bot
        """
        return await self._client.call_method('toggleBusinessConnectedBotChatIsPaused', {'@type': 'toggleBusinessConnectedBotChatIsPaused', 'chat_id': chat_id, 'is_paused': is_paused})

    async def remove_business_connected_bot_from_chat(self, chat_id: int = None) -> Ok:
        """
        description Removes the connected business bot from a specific chat by adding the chat to businessRecipients.excluded_chat_ids @chat_id Chat identifier
        """
        return await self._client.call_method('removeBusinessConnectedBotFromChat', {'@type': 'removeBusinessConnectedBotFromChat', 'chat_id': chat_id})

    async def get_business_chat_links(self) -> BusinessChatLinks:
        """
        description Returns business chat links created for the current account
        """
        return await self._client.call_method('getBusinessChatLinks', {'@type': 'getBusinessChatLinks'})

    async def create_business_chat_link(self, link_info: inputBusinessChatLink = None) -> BusinessChatLink:
        """
        description Creates a business chat link for the current account. Requires Telegram Business subscription. There can be up to getOption("business_chat_link_count_max") links created. Returns the created link
        link_info Information about the link to create
        """
        return await self._client.call_method('createBusinessChatLink', {'@type': 'createBusinessChatLink', 'link_info': link_info})

    async def edit_business_chat_link(self, link: str = None, link_info: inputBusinessChatLink = None) -> BusinessChatLink:
        """
        description Edits a business chat link of the current account. Requires Telegram Business subscription. Returns the edited link
        link The link to edit
        link_info New description of the link
        """
        return await self._client.call_method('editBusinessChatLink', {'@type': 'editBusinessChatLink', 'link': link, 'link_info': link_info})

    async def delete_business_chat_link(self, link: str = None) -> Ok:
        """
        description Deletes a business chat link of the current account @link The link to delete
        """
        return await self._client.call_method('deleteBusinessChatLink', {'@type': 'deleteBusinessChatLink', 'link': link})

    async def get_business_chat_link_info(self, link_name: str = None) -> BusinessChatLinkInfo:
        """
        description Returns information about a business chat link @link_name Name of the link
        """
        return await self._client.call_method('getBusinessChatLinkInfo', {'@type': 'getBusinessChatLinkInfo', 'link_name': link_name})

    async def get_user_link(self) -> UserLink:
        """
        description Returns an HTTPS link, which can be used to get information about the current user
        """
        return await self._client.call_method('getUserLink', {'@type': 'getUserLink'})

    async def search_user_by_token(self, token: str = None) -> User:
        """
        description Searches a user by a token from the user's link @token Token to search for
        """
        return await self._client.call_method('searchUserByToken', {'@type': 'searchUserByToken', 'token': token})

    async def set_commands(self, scope: BotCommandScope = None, language_code: str = None, commands: List[botCommand] = None) -> Ok:
        """
        description Sets the list of commands supported by the bot for the given user scope and language; for bots only
        scope The scope to which the commands are relevant; pass null to change commands in the default bot command scope
        language_code A two-letter ISO 639-1 language code. If empty, the commands will be applied to all users from the given scope, for which language there are no dedicated commands
        commands List of the bot's commands
        """
        return await self._client.call_method('setCommands', {'@type': 'setCommands', 'scope': scope, 'language_code': language_code, 'commands': commands})

    async def delete_commands(self, scope: BotCommandScope = None, language_code: str = None) -> Ok:
        """
        description Deletes commands supported by the bot for the given user scope and language; for bots only
        scope The scope to which the commands are relevant; pass null to delete commands in the default bot command scope
        language_code A two-letter ISO 639-1 language code or an empty string
        """
        return await self._client.call_method('deleteCommands', {'@type': 'deleteCommands', 'scope': scope, 'language_code': language_code})

    async def get_commands(self, scope: BotCommandScope = None, language_code: str = None) -> BotCommands:
        """
        description Returns the list of commands supported by the bot for the given user scope and language; for bots only
        scope The scope to which the commands are relevant; pass null to get commands in the default bot command scope
        language_code A two-letter ISO 639-1 language code or an empty string
        """
        return await self._client.call_method('getCommands', {'@type': 'getCommands', 'scope': scope, 'language_code': language_code})

    async def set_menu_button(self, user_id: int = None, menu_button: botMenuButton = None) -> Ok:
        """
        description Sets menu button for the given user or for all users; for bots only
        user_id Identifier of the user or 0 to set menu button for all users
        menu_button New menu button
        """
        return await self._client.call_method('setMenuButton', {'@type': 'setMenuButton', 'user_id': user_id, 'menu_button': menu_button})

    async def get_menu_button(self, user_id: int = None) -> BotMenuButton:
        """
        description Returns menu button set by the bot for the given user; for bots only @user_id Identifier of the user or 0 to get the default menu button
        """
        return await self._client.call_method('getMenuButton', {'@type': 'getMenuButton', 'user_id': user_id})

    async def set_default_group_administrator_rights(self, default_group_administrator_rights: chatAdministratorRights = None) -> Ok:
        """
        description Sets default administrator rights for adding the bot to basic group and supergroup chats; for bots only @default_group_administrator_rights Default administrator rights for adding the bot to basic group and supergroup chats; pass null to remove default rights
        """
        return await self._client.call_method('setDefaultGroupAdministratorRights', {'@type': 'setDefaultGroupAdministratorRights', 'default_group_administrator_rights': default_group_administrator_rights})

    async def set_default_channel_administrator_rights(self, default_channel_administrator_rights: chatAdministratorRights = None) -> Ok:
        """
        description Sets default administrator rights for adding the bot to channel chats; for bots only @default_channel_administrator_rights Default administrator rights for adding the bot to channels; pass null to remove default rights
        """
        return await self._client.call_method('setDefaultChannelAdministratorRights', {'@type': 'setDefaultChannelAdministratorRights', 'default_channel_administrator_rights': default_channel_administrator_rights})

    async def can_bot_send_messages(self, bot_user_id: int = None) -> Ok:
        """
        description Checks whether the specified bot can send messages to the user. Returns a 404 error if can't and the access can be granted by call to allowBotToSendMessages @bot_user_id Identifier of the target bot
        """
        return await self._client.call_method('canBotSendMessages', {'@type': 'canBotSendMessages', 'bot_user_id': bot_user_id})

    async def allow_bot_to_send_messages(self, bot_user_id: int = None) -> Ok:
        """
        description Allows the specified bot to send messages to the user @bot_user_id Identifier of the target bot
        """
        return await self._client.call_method('allowBotToSendMessages', {'@type': 'allowBotToSendMessages', 'bot_user_id': bot_user_id})

    async def send_web_app_custom_request(self, bot_user_id: int = None, method: str = None, parameters: str = None) -> CustomRequestResult:
        """
        description Sends a custom request from a Web App
        bot_user_id Identifier of the bot
        method The method name
        parameters JSON-serialized method parameters
        """
        return await self._client.call_method('sendWebAppCustomRequest', {'@type': 'sendWebAppCustomRequest', 'bot_user_id': bot_user_id, 'method': method, 'parameters': parameters})

    async def get_bot_media_previews(self, bot_user_id: int = None) -> BotMediaPreviews:
        """
        description Returns the list of media previews of a bot @bot_user_id Identifier of the target bot. The bot must have the main Web App
        """
        return await self._client.call_method('getBotMediaPreviews', {'@type': 'getBotMediaPreviews', 'bot_user_id': bot_user_id})

    async def get_bot_media_preview_info(self, bot_user_id: int = None, language_code: str = None) -> BotMediaPreviewInfo:
        """
        description Returns the list of media previews for the given language and the list of languages for which the bot has dedicated previews
        bot_user_id Identifier of the target bot. The bot must be owned and must have the main Web App
        language_code A two-letter ISO 639-1 language code for which to get previews. If empty, then default previews are returned
        """
        return await self._client.call_method('getBotMediaPreviewInfo', {'@type': 'getBotMediaPreviewInfo', 'bot_user_id': bot_user_id, 'language_code': language_code})

    async def add_bot_media_preview(self, bot_user_id: int = None, language_code: str = None, content: InputStoryContent = None) -> BotMediaPreview:
        """
        description Adds a new media preview to the beginning of the list of media previews of a bot. Returns the added preview after addition is completed server-side. The total number of previews must not exceed getOption("bot_media_preview_count_max") for the given language
        bot_user_id Identifier of the target bot. The bot must be owned and must have the main Web App
        language_code A two-letter ISO 639-1 language code for which preview is added. If empty, then the preview will be shown to all users for whose languages there are no dedicated previews.
        content Content of the added preview
        """
        return await self._client.call_method('addBotMediaPreview', {'@type': 'addBotMediaPreview', 'bot_user_id': bot_user_id, 'language_code': language_code, 'content': content})

    async def edit_bot_media_preview(self, bot_user_id: int = None, language_code: str = None, file_id: int = None, content: InputStoryContent = None) -> BotMediaPreview:
        """
        description Replaces media preview in the list of media previews of a bot. Returns the new preview after edit is completed server-side
        bot_user_id Identifier of the target bot. The bot must be owned and must have the main Web App
        language_code Language code of the media preview to edit
        file_id File identifier of the media to replace
        content Content of the new preview
        """
        return await self._client.call_method('editBotMediaPreview', {'@type': 'editBotMediaPreview', 'bot_user_id': bot_user_id, 'language_code': language_code, 'file_id': file_id, 'content': content})

    async def reorder_bot_media_previews(self, bot_user_id: int = None, language_code: str = None, file_ids: List[int] = None) -> Ok:
        """
        description Changes order of media previews in the list of media previews of a bot
        bot_user_id Identifier of the target bot. The bot must be owned and must have the main Web App
        language_code Language code of the media previews to reorder
        file_ids File identifiers of the media in the new order
        """
        return await self._client.call_method('reorderBotMediaPreviews', {'@type': 'reorderBotMediaPreviews', 'bot_user_id': bot_user_id, 'language_code': language_code, 'file_ids': file_ids})

    async def delete_bot_media_previews(self, bot_user_id: int = None, language_code: str = None, file_ids: List[int] = None) -> Ok:
        """
        description Deletes media previews from the list of media previews of a bot
        bot_user_id Identifier of the target bot. The bot must be owned and must have the main Web App
        language_code Language code of the media previews to delete
        file_ids File identifiers of the media to delete
        """
        return await self._client.call_method('deleteBotMediaPreviews', {'@type': 'deleteBotMediaPreviews', 'bot_user_id': bot_user_id, 'language_code': language_code, 'file_ids': file_ids})

    async def check_bot_username(self, username: str = None) -> CheckChatUsernameResult:
        """
        description Checks whether a username can be set for a new bot. Use checkChatUsername to check username for other chat types
        username Username to be checked
        """
        return await self._client.call_method('checkBotUsername', {'@type': 'checkBotUsername', 'username': username})

    async def create_bot(self, manager_bot_user_id: int = None, name: str = None, username: str = None, via_link: bool = None) -> User:
        """
        description Creates a bot which will be managed by another bot. Returns the created bot. May return an error with a message "BOT_CREATE_LIMIT_EXCEEDED"
        manager_bot_user_id Identifier of the bot that will manage the created bot
        name Name of the bot; 1-64 characters
        username Username of the bot. The username must end with "bot". Use checkBotUsername to find whether the name is suitable
        via_link Pass true if the bot is created from an internalLinkTypeRequestManagedBot link
        """
        return await self._client.call_method('createBot', {'@type': 'createBot', 'manager_bot_user_id': manager_bot_user_id, 'name': name, 'username': username, 'via_link': via_link})

    async def get_managed_bot_token(self, bot_user_id: int = None, revoke: bool = None) -> Text:
        """
        description Returns token of a managed bot; for bots only
        bot_user_id Identifier of the managed bot
        revoke Pass true to revoke the current token and create a new one
        """
        return await self._client.call_method('getManagedBotToken', {'@type': 'getManagedBotToken', 'bot_user_id': bot_user_id, 'revoke': revoke})

    async def get_managed_bot_access_settings(self, bot_user_id: int = None) -> BotAccessSettings:
        """
        description Returns access settings of a managed bot; for bots only @bot_user_id Identifier of the managed bot
        """
        return await self._client.call_method('getManagedBotAccessSettings', {'@type': 'getManagedBotAccessSettings', 'bot_user_id': bot_user_id})

    async def set_managed_bot_access_settings(self, bot_user_id: int = None, settings: botAccessSettings = None) -> Ok:
        """
        description Sets access settings of a managed bot; for bots only @bot_user_id Identifier of the managed bot @settings New access settings
        """
        return await self._client.call_method('setManagedBotAccessSettings', {'@type': 'setManagedBotAccessSettings', 'bot_user_id': bot_user_id, 'settings': settings})

    async def set_bot_name(self, bot_user_id: int = None, language_code: str = None, name: str = None) -> Ok:
        """
        description Sets the name of a bot. Can be called only if userTypeBot.can_be_edited == true
        bot_user_id Identifier of the target bot
        language_code A two-letter ISO 639-1 language code. If empty, the name will be shown to all users for whose languages there is no dedicated name
        name New bot's name on the specified language; 0-64 characters; must be non-empty if language code is empty
        """
        return await self._client.call_method('setBotName', {'@type': 'setBotName', 'bot_user_id': bot_user_id, 'language_code': language_code, 'name': name})

    async def get_bot_name(self, bot_user_id: int = None, language_code: str = None) -> Text:
        """
        description Returns the name of a bot in the given language. Can be called only if userTypeBot.can_be_edited == true
        bot_user_id Identifier of the target bot
        language_code A two-letter ISO 639-1 language code or an empty string
        """
        return await self._client.call_method('getBotName', {'@type': 'getBotName', 'bot_user_id': bot_user_id, 'language_code': language_code})

    async def set_bot_profile_photo(self, bot_user_id: int = None, photo: InputChatPhoto = None) -> Ok:
        """
        description Changes a profile photo for a bot @bot_user_id Identifier of the target bot @photo Profile photo to set; pass null to delete the chat photo
        """
        return await self._client.call_method('setBotProfilePhoto', {'@type': 'setBotProfilePhoto', 'bot_user_id': bot_user_id, 'photo': photo})

    async def toggle_bot_username_is_active(self, bot_user_id: int = None, username: str = None, is_active: bool = None) -> Ok:
        """
        description Changes active state for a username of a bot. The editable username can be disabled only if there are other active usernames.
        bot_user_id Identifier of the target bot
        username The username to change
        is_active Pass true to activate the username; pass false to disable it
        """
        return await self._client.call_method('toggleBotUsernameIsActive', {'@type': 'toggleBotUsernameIsActive', 'bot_user_id': bot_user_id, 'username': username, 'is_active': is_active})

    async def reorder_bot_active_usernames(self, bot_user_id: int = None, usernames: List[str] = None) -> Ok:
        """
        description Changes order of active usernames of a bot. Can be called only if userTypeBot.can_be_edited == true @bot_user_id Identifier of the target bot @usernames The new order of active usernames. All currently active usernames must be specified
        """
        return await self._client.call_method('reorderBotActiveUsernames', {'@type': 'reorderBotActiveUsernames', 'bot_user_id': bot_user_id, 'usernames': usernames})

    async def set_bot_info_description(self, bot_user_id: int = None, language_code: str = None, description: str = None) -> Ok:
        """
        description Sets the text shown in the chat with a bot if the chat is empty. Can be called only if userTypeBot.can_be_edited == true
        bot_user_id Identifier of the target bot
        language_code A two-letter ISO 639-1 language code. If empty, the description will be shown to all users for whose languages there is no dedicated description
        param_description New bot's description on the specified language
        """
        return await self._client.call_method('setBotInfoDescription', {'@type': 'setBotInfoDescription', 'bot_user_id': bot_user_id, 'language_code': language_code, 'description': description})

    async def get_bot_info_description(self, bot_user_id: int = None, language_code: str = None) -> Text:
        """
        description Returns the text shown in the chat with a bot if the chat is empty in the given language. Can be called only if userTypeBot.can_be_edited == true
        bot_user_id Identifier of the target bot
        language_code A two-letter ISO 639-1 language code or an empty string
        """
        return await self._client.call_method('getBotInfoDescription', {'@type': 'getBotInfoDescription', 'bot_user_id': bot_user_id, 'language_code': language_code})

    async def set_bot_info_short_description(self, bot_user_id: int = None, language_code: str = None, short_description: str = None) -> Ok:
        """
        description Sets the text shown on a bot's profile page and sent together with the link when users share the bot. Can be called only if userTypeBot.can_be_edited == true
        bot_user_id Identifier of the target bot
        language_code A two-letter ISO 639-1 language code. If empty, the short description will be shown to all users for whose languages there is no dedicated description
        short_description New bot's short description on the specified language
        """
        return await self._client.call_method('setBotInfoShortDescription', {'@type': 'setBotInfoShortDescription', 'bot_user_id': bot_user_id, 'language_code': language_code, 'short_description': short_description})

    async def get_bot_info_short_description(self, bot_user_id: int = None, language_code: str = None) -> Text:
        """
        description Returns the text shown on a bot's profile page and sent together with the link when users share the bot in the given language. Can be called only if userTypeBot.can_be_edited == true
        bot_user_id Identifier of the target bot
        language_code A two-letter ISO 639-1 language code or an empty string
        """
        return await self._client.call_method('getBotInfoShortDescription', {'@type': 'getBotInfoShortDescription', 'bot_user_id': bot_user_id, 'language_code': language_code})

    async def set_message_sender_bot_verification(self, bot_user_id: int = None, verified_id: MessageSender = None, custom_description: str = None) -> Ok:
        """
        description Changes the verification status of a user or a chat by an owned bot
        bot_user_id Identifier of the owned bot, which will verify the user or the chat
        verified_id Identifier of the user or the supergroup or channel chat, which will be verified by the bot
        custom_description Custom description of verification reason; 0-getOption("bot_verification_custom_description_length_max").
        """
        return await self._client.call_method('setMessageSenderBotVerification', {'@type': 'setMessageSenderBotVerification', 'bot_user_id': bot_user_id, 'verified_id': verified_id, 'custom_description': custom_description})

    async def remove_message_sender_bot_verification(self, bot_user_id: int = None, verified_id: MessageSender = None) -> Ok:
        """
        description Removes the verification status of a user or a chat by an owned bot
        bot_user_id Identifier of the owned bot, which verified the user or the chat
        verified_id Identifier of the user or the supergroup or channel chat, which verification is removed
        """
        return await self._client.call_method('removeMessageSenderBotVerification', {'@type': 'removeMessageSenderBotVerification', 'bot_user_id': bot_user_id, 'verified_id': verified_id})

    async def get_active_sessions(self) -> Sessions:
        """
        description Returns all active sessions of the current user. Additionally, getBusinessConnectedBot must be used to show the bot on top of active sessions
        """
        return await self._client.call_method('getActiveSessions', {'@type': 'getActiveSessions'})

    async def terminate_session(self, session_id: int = None) -> Ok:
        """
        description Terminates a session of the current user @session_id Session identifier
        """
        return await self._client.call_method('terminateSession', {'@type': 'terminateSession', 'session_id': session_id})

    async def terminate_all_other_sessions(self) -> Ok:
        """
        description Terminates all other sessions of the current user. Additionally, the user must be suggested to delete the connected business bot using deleteBusinessConnectedBot if there is any
        """
        return await self._client.call_method('terminateAllOtherSessions', {'@type': 'terminateAllOtherSessions'})

    async def confirm_session(self, session_id: int = None) -> Ok:
        """
        description Confirms an unconfirmed session of the current user from another device @session_id Session identifier
        """
        return await self._client.call_method('confirmSession', {'@type': 'confirmSession', 'session_id': session_id})

    async def toggle_session_can_accept_calls(self, session_id: int = None, can_accept_calls: bool = None) -> Ok:
        """
        description Toggles whether a session can accept incoming calls @session_id Session identifier @can_accept_calls Pass true to allow accepting incoming calls by the session; pass false otherwise
        """
        return await self._client.call_method('toggleSessionCanAcceptCalls', {'@type': 'toggleSessionCanAcceptCalls', 'session_id': session_id, 'can_accept_calls': can_accept_calls})

    async def toggle_session_can_accept_secret_chats(self, session_id: int = None, can_accept_secret_chats: bool = None) -> Ok:
        """
        description Toggles whether a session can accept incoming secret chats @session_id Session identifier @can_accept_secret_chats Pass true to allow accepting secret chats by the session; pass false otherwise
        """
        return await self._client.call_method('toggleSessionCanAcceptSecretChats', {'@type': 'toggleSessionCanAcceptSecretChats', 'session_id': session_id, 'can_accept_secret_chats': can_accept_secret_chats})

    async def set_inactive_session_ttl(self, inactive_session_ttl_days: int = None) -> Ok:
        """
        description Changes the period of inactivity after which sessions will automatically be terminated @inactive_session_ttl_days New number of days of inactivity before sessions will be automatically terminated; 1-366 days
        """
        return await self._client.call_method('setInactiveSessionTtl', {'@type': 'setInactiveSessionTtl', 'inactive_session_ttl_days': inactive_session_ttl_days})

    async def get_connected_websites(self) -> ConnectedWebsites:
        """
        description Returns all website where the current user used Telegram to log in
        """
        return await self._client.call_method('getConnectedWebsites', {'@type': 'getConnectedWebsites'})

    async def disconnect_website(self, website_id: int = None) -> Ok:
        """
        description Disconnects website from the current user's Telegram account @website_id Website identifier
        """
        return await self._client.call_method('disconnectWebsite', {'@type': 'disconnectWebsite', 'website_id': website_id})

    async def disconnect_all_websites(self) -> Ok:
        """
        description Disconnects all websites from the current user's Telegram account
        """
        return await self._client.call_method('disconnectAllWebsites', {'@type': 'disconnectAllWebsites'})

    async def set_supergroup_username(self, supergroup_id: int = None, username: str = None) -> Ok:
        """
        description Changes the editable username of a supergroup or channel, requires owner privileges in the supergroup or channel
        supergroup_id Identifier of the supergroup or channel
        username New value of the username. Use an empty string to remove the username. The username can't be completely removed if there is another active or disabled username
        """
        return await self._client.call_method('setSupergroupUsername', {'@type': 'setSupergroupUsername', 'supergroup_id': supergroup_id, 'username': username})

    async def toggle_supergroup_username_is_active(self, supergroup_id: int = None, username: str = None, is_active: bool = None) -> Ok:
        """
        description Changes active state for a username of a supergroup or channel, requires owner privileges in the supergroup or channel. The editable username can't be disabled.
        supergroup_id Identifier of the supergroup or channel
        username The username to change
        is_active Pass true to activate the username; pass false to disable it
        """
        return await self._client.call_method('toggleSupergroupUsernameIsActive', {'@type': 'toggleSupergroupUsernameIsActive', 'supergroup_id': supergroup_id, 'username': username, 'is_active': is_active})

    async def disable_all_supergroup_usernames(self, supergroup_id: int = None) -> Ok:
        """
        description Disables all active non-editable usernames of a supergroup or channel, requires owner privileges in the supergroup or channel @supergroup_id Identifier of the supergroup or channel
        """
        return await self._client.call_method('disableAllSupergroupUsernames', {'@type': 'disableAllSupergroupUsernames', 'supergroup_id': supergroup_id})

    async def reorder_supergroup_active_usernames(self, supergroup_id: int = None, usernames: List[str] = None) -> Ok:
        """
        description Changes order of active usernames of a supergroup or channel, requires owner privileges in the supergroup or channel
        supergroup_id Identifier of the supergroup or channel
        usernames The new order of active usernames. All currently active usernames must be specified
        """
        return await self._client.call_method('reorderSupergroupActiveUsernames', {'@type': 'reorderSupergroupActiveUsernames', 'supergroup_id': supergroup_id, 'usernames': usernames})

    async def set_supergroup_sticker_set(self, supergroup_id: int = None, sticker_set_id: int = None) -> Ok:
        """
        description Changes the sticker set of a supergroup; requires can_change_info administrator right @supergroup_id Identifier of the supergroup @sticker_set_id New value of the supergroup sticker set identifier. Use 0 to remove the supergroup sticker set
        """
        return await self._client.call_method('setSupergroupStickerSet', {'@type': 'setSupergroupStickerSet', 'supergroup_id': supergroup_id, 'sticker_set_id': sticker_set_id})

    async def set_supergroup_custom_emoji_sticker_set(self, supergroup_id: int = None, custom_emoji_sticker_set_id: int = None) -> Ok:
        """
        description Changes the custom emoji sticker set of a supergroup; requires can_change_info administrator right. The chat must have at least chatBoostFeatures.min_custom_emoji_sticker_set_boost_level boost level to pass the corresponding color
        supergroup_id Identifier of the supergroup
        custom_emoji_sticker_set_id New value of the custom emoji sticker set identifier for the supergroup. Use 0 to remove the custom emoji sticker set in the supergroup
        """
        return await self._client.call_method('setSupergroupCustomEmojiStickerSet', {'@type': 'setSupergroupCustomEmojiStickerSet', 'supergroup_id': supergroup_id, 'custom_emoji_sticker_set_id': custom_emoji_sticker_set_id})

    async def set_supergroup_unrestrict_boost_count(self, supergroup_id: int = None, unrestrict_boost_count: int = None) -> Ok:
        """
        description Changes the number of times the supergroup must be boosted by a user to ignore slow mode and chat permission restrictions; requires can_restrict_members administrator right
        supergroup_id Identifier of the supergroup
        unrestrict_boost_count New value of the unrestrict_boost_count supergroup setting; 0-8. Use 0 to remove the setting
        """
        return await self._client.call_method('setSupergroupUnrestrictBoostCount', {'@type': 'setSupergroupUnrestrictBoostCount', 'supergroup_id': supergroup_id, 'unrestrict_boost_count': unrestrict_boost_count})

    async def set_supergroup_main_profile_tab(self, supergroup_id: int = None, main_profile_tab: ProfileTab = None) -> Ok:
        """
        description Changes the main profile tab of the channel; requires can_change_info administrator right
        supergroup_id Identifier of the channel
        main_profile_tab The new value of the main profile tab
        """
        return await self._client.call_method('setSupergroupMainProfileTab', {'@type': 'setSupergroupMainProfileTab', 'supergroup_id': supergroup_id, 'main_profile_tab': main_profile_tab})

    async def toggle_supergroup_sign_messages(self, supergroup_id: int = None, sign_messages: bool = None, show_message_sender: bool = None) -> Ok:
        """
        description Toggles whether sender signature or link to the account is added to sent messages in a channel; requires can_change_info member right
        supergroup_id Identifier of the channel
        sign_messages New value of sign_messages
        show_message_sender New value of show_message_sender
        """
        return await self._client.call_method('toggleSupergroupSignMessages', {'@type': 'toggleSupergroupSignMessages', 'supergroup_id': supergroup_id, 'sign_messages': sign_messages, 'show_message_sender': show_message_sender})

    async def toggle_supergroup_join_to_send_messages(self, supergroup_id: int = None, join_to_send_messages: bool = None) -> Ok:
        """
        description Toggles whether joining is mandatory to send messages to a discussion supergroup; requires can_restrict_members administrator right
        supergroup_id Identifier of the supergroup that isn't a broadcast group
        join_to_send_messages New value of join_to_send_messages
        """
        return await self._client.call_method('toggleSupergroupJoinToSendMessages', {'@type': 'toggleSupergroupJoinToSendMessages', 'supergroup_id': supergroup_id, 'join_to_send_messages': join_to_send_messages})

    async def toggle_supergroup_join_by_request(self, supergroup_id: int = None, join_by_request: bool = None, guard_bot_user_id: int = None, apply_to_invite_links: bool = None) -> Ok:
        """
        description Toggles whether all users directly joining the supergroup need to be approved by supergroup administrators; requires can_restrict_members administrator right
        supergroup_id Identifier of the supergroup that isn't a broadcast group and isn't a channel direct message group
        join_by_request New value of join_by_request
        guard_bot_user_id Identifier of the bot which will be the guard bot in the group; pass 0 if none; ignored if join_by_request == false.
        apply_to_invite_links Pass true to apply the change to the existing invite links, including primary links
        """
        return await self._client.call_method('toggleSupergroupJoinByRequest', {'@type': 'toggleSupergroupJoinByRequest', 'supergroup_id': supergroup_id, 'join_by_request': join_by_request, 'guard_bot_user_id': guard_bot_user_id, 'apply_to_invite_links': apply_to_invite_links})

    async def toggle_supergroup_is_all_history_available(self, supergroup_id: int = None, is_all_history_available: bool = None) -> Ok:
        """
        description Toggles whether the message history of a supergroup is available to new members; requires can_change_info member right @supergroup_id The identifier of the supergroup @is_all_history_available The new value of is_all_history_available
        """
        return await self._client.call_method('toggleSupergroupIsAllHistoryAvailable', {'@type': 'toggleSupergroupIsAllHistoryAvailable', 'supergroup_id': supergroup_id, 'is_all_history_available': is_all_history_available})

    async def toggle_supergroup_can_have_sponsored_messages(self, supergroup_id: int = None, can_have_sponsored_messages: bool = None) -> Ok:
        """
        description Toggles whether sponsored messages are shown in the channel chat; requires owner privileges in the channel. The chat must have at least chatBoostFeatures.min_sponsored_message_disable_boost_level boost level to disable sponsored messages
        supergroup_id The identifier of the channel
        can_have_sponsored_messages The new value of can_have_sponsored_messages
        """
        return await self._client.call_method('toggleSupergroupCanHaveSponsoredMessages', {'@type': 'toggleSupergroupCanHaveSponsoredMessages', 'supergroup_id': supergroup_id, 'can_have_sponsored_messages': can_have_sponsored_messages})

    async def toggle_supergroup_has_automatic_translation(self, supergroup_id: int = None, has_automatic_translation: bool = None) -> Ok:
        """
        description Toggles whether messages are automatically translated in the channel chat; requires can_change_info administrator right in the channel.
        supergroup_id The identifier of the channel
        has_automatic_translation The new value of has_automatic_translation
        """
        return await self._client.call_method('toggleSupergroupHasAutomaticTranslation', {'@type': 'toggleSupergroupHasAutomaticTranslation', 'supergroup_id': supergroup_id, 'has_automatic_translation': has_automatic_translation})

    async def toggle_supergroup_has_hidden_members(self, supergroup_id: int = None, has_hidden_members: bool = None) -> Ok:
        """
        description Toggles whether non-administrators can receive only administrators and bots using getSupergroupMembers or searchChatMembers. Can be called only if supergroupFullInfo.can_hide_members == true
        supergroup_id Identifier of the supergroup
        has_hidden_members New value of has_hidden_members
        """
        return await self._client.call_method('toggleSupergroupHasHiddenMembers', {'@type': 'toggleSupergroupHasHiddenMembers', 'supergroup_id': supergroup_id, 'has_hidden_members': has_hidden_members})

    async def toggle_supergroup_has_aggressive_anti_spam_enabled(self, supergroup_id: int = None, has_aggressive_anti_spam_enabled: bool = None) -> Ok:
        """
        description Toggles whether aggressive anti-spam checks are enabled in the supergroup. Can be called only if supergroupFullInfo.can_toggle_aggressive_anti_spam == true
        supergroup_id The identifier of the supergroup, which isn't a broadcast group
        has_aggressive_anti_spam_enabled The new value of has_aggressive_anti_spam_enabled
        """
        return await self._client.call_method('toggleSupergroupHasAggressiveAntiSpamEnabled', {'@type': 'toggleSupergroupHasAggressiveAntiSpamEnabled', 'supergroup_id': supergroup_id, 'has_aggressive_anti_spam_enabled': has_aggressive_anti_spam_enabled})

    async def toggle_supergroup_is_forum(self, supergroup_id: int = None, is_forum: bool = None, has_forum_tabs: bool = None) -> Ok:
        """
        description Toggles whether the supergroup is a forum; requires owner privileges in the supergroup. Discussion supergroups can't be converted to forums
        supergroup_id Identifier of the supergroup
        is_forum New value of is_forum
        has_forum_tabs New value of has_forum_tabs; ignored if is_forum is false
        """
        return await self._client.call_method('toggleSupergroupIsForum', {'@type': 'toggleSupergroupIsForum', 'supergroup_id': supergroup_id, 'is_forum': is_forum, 'has_forum_tabs': has_forum_tabs})

    async def toggle_supergroup_is_broadcast_group(self, supergroup_id: int = None) -> Ok:
        """
        description Upgrades supergroup to a broadcast group; requires owner privileges in the supergroup @supergroup_id Identifier of the supergroup
        """
        return await self._client.call_method('toggleSupergroupIsBroadcastGroup', {'@type': 'toggleSupergroupIsBroadcastGroup', 'supergroup_id': supergroup_id})

    async def report_supergroup_spam(self, supergroup_id: int = None, message_ids: List[int] = None) -> Ok:
        """
        description Reports messages in a supergroup as spam; requires administrator rights in the supergroup
        supergroup_id Supergroup identifier
        message_ids Identifiers of messages to report. Use messageProperties.can_report_supergroup_spam to check whether the message can be reported
        """
        return await self._client.call_method('reportSupergroupSpam', {'@type': 'reportSupergroupSpam', 'supergroup_id': supergroup_id, 'message_ids': message_ids})

    async def report_supergroup_anti_spam_false_positive(self, supergroup_id: int = None, message_id: int = None) -> Ok:
        """
        description Reports a false deletion of a message by aggressive anti-spam checks; requires administrator rights in the supergroup. Can be called only for messages from chatEventMessageDeleted with can_report_anti_spam_false_positive == true
        supergroup_id Supergroup identifier
        message_id Identifier of the erroneously deleted message from chatEventMessageDeleted
        """
        return await self._client.call_method('reportSupergroupAntiSpamFalsePositive', {'@type': 'reportSupergroupAntiSpamFalsePositive', 'supergroup_id': supergroup_id, 'message_id': message_id})

    async def get_supergroup_members(self, supergroup_id: int = None, filter: SupergroupMembersFilter = None, offset: int = None, limit: int = None) -> ChatMembers:
        """
        description Returns information about members or banned users in a supergroup or channel. Can be used only if supergroupFullInfo.can_get_members == true; additionally, administrator privileges may be required for some filters
        supergroup_id Identifier of the supergroup or channel
        filter The type of users to return; pass null to use supergroupMembersFilterRecent
        offset Number of users to skip
        limit The maximum number of users to be returned; up to 200
        """
        return await self._client.call_method('getSupergroupMembers', {'@type': 'getSupergroupMembers', 'supergroup_id': supergroup_id, 'filter': filter, 'offset': offset, 'limit': limit})

    async def close_secret_chat(self, secret_chat_id: int = None) -> Ok:
        """
        description Closes a secret chat, effectively transferring its state to secretChatStateClosed @secret_chat_id Secret chat identifier
        """
        return await self._client.call_method('closeSecretChat', {'@type': 'closeSecretChat', 'secret_chat_id': secret_chat_id})

    async def get_chat_event_log(self, chat_id: int = None, query: str = None, from_event_id: int = None, limit: int = None, filters: chatEventLogFilters = None, user_ids: List[int] = None) -> ChatEvents:
        """
        description Returns a list of service actions taken by chat members and administrators in the last 48 hours. Available only for supergroups and channels. Requires administrator rights. Returns results in reverse chronological order (i.e., in order of decreasing event_id)
        chat_id Chat identifier
        query Search query by which to filter events
        from_event_id Identifier of an event from which to return results. Use 0 to get results from the latest events
        limit The maximum number of events to return; up to 100
        filters The types of events to return; pass null to get chat events of all types
        user_ids User identifiers by which to filter events. By default, events relating to all users will be returned
        """
        return await self._client.call_method('getChatEventLog', {'@type': 'getChatEventLog', 'chat_id': chat_id, 'query': query, 'from_event_id': from_event_id, 'limit': limit, 'filters': filters, 'user_ids': user_ids})

    async def get_time_zones(self) -> TimeZones:
        """
        description Returns the list of supported time zones
        """
        return await self._client.call_method('getTimeZones', {'@type': 'getTimeZones'})

    async def get_payment_form(self, input_invoice: InputInvoice = None, theme: themeParameters = None) -> PaymentForm:
        """
        description Returns an invoice payment form. This method must be called when the user presses inline button of the type inlineKeyboardButtonTypeBuy, or wants to buy access to media in a messagePaidMedia message
        input_invoice The invoice
        theme Preferred payment form theme; pass null to use the default theme
        """
        return await self._client.call_method('getPaymentForm', {'@type': 'getPaymentForm', 'input_invoice': input_invoice, 'theme': theme})

    async def validate_order_info(self, input_invoice: InputInvoice = None, order_info: orderInfo = None, allow_save: bool = None) -> ValidatedOrderInfo:
        """
        description Validates the order information provided by a user and returns the available shipping options for a flexible invoice
        input_invoice The invoice
        order_info The order information, provided by the user; pass null if empty
        allow_save Pass true to save the order information
        """
        return await self._client.call_method('validateOrderInfo', {'@type': 'validateOrderInfo', 'input_invoice': input_invoice, 'order_info': order_info, 'allow_save': allow_save})

    async def send_payment_form(self, input_invoice: InputInvoice = None, payment_form_id: int = None, order_info_id: str = None, shipping_option_id: str = None, credentials: InputCredentials = None, tip_amount: int = None) -> PaymentResult:
        """
        description Sends a filled-out payment form to the bot for final verification
        input_invoice The invoice
        payment_form_id Payment form identifier returned by getPaymentForm
        order_info_id Identifier returned by validateOrderInfo, or an empty string
        shipping_option_id Identifier of a chosen shipping option, if applicable
        credentials The credentials chosen by user for payment; pass null for a payment in Telegram Stars
        tip_amount Chosen by the user amount of tip in the smallest units of the currency
        """
        return await self._client.call_method('sendPaymentForm', {'@type': 'sendPaymentForm', 'input_invoice': input_invoice, 'payment_form_id': payment_form_id, 'order_info_id': order_info_id, 'shipping_option_id': shipping_option_id, 'credentials': credentials, 'tip_amount': tip_amount})

    async def get_payment_receipt(self, chat_id: int = None, message_id: int = None) -> PaymentReceipt:
        """
        description Returns information about a successful payment @chat_id Chat identifier of the messagePaymentSuccessful message @message_id Message identifier
        """
        return await self._client.call_method('getPaymentReceipt', {'@type': 'getPaymentReceipt', 'chat_id': chat_id, 'message_id': message_id})

    async def get_saved_order_info(self) -> OrderInfo:
        """
        description Returns saved order information. Returns a 404 error if there is no saved order information
        """
        return await self._client.call_method('getSavedOrderInfo', {'@type': 'getSavedOrderInfo'})

    async def delete_saved_order_info(self) -> Ok:
        """
        description Deletes saved order information
        """
        return await self._client.call_method('deleteSavedOrderInfo', {'@type': 'deleteSavedOrderInfo'})

    async def delete_saved_credentials(self) -> Ok:
        """
        description Deletes saved credentials for all payment provider bots
        """
        return await self._client.call_method('deleteSavedCredentials', {'@type': 'deleteSavedCredentials'})

    async def set_gift_settings(self, settings: giftSettings = None) -> Ok:
        """
        description Changes settings for gift receiving for the current user @settings The new settings
        """
        return await self._client.call_method('setGiftSettings', {'@type': 'setGiftSettings', 'settings': settings})

    async def get_available_gifts(self) -> AvailableGifts:
        """
        description Returns gifts that can be sent to other users and channel chats
        """
        return await self._client.call_method('getAvailableGifts', {'@type': 'getAvailableGifts'})

    async def can_send_gift(self, gift_id: int = None) -> CanSendGiftResult:
        """
        description Checks whether a gift with next_send_date in the future can be sent already
        gift_id Identifier of the gift to send
        """
        return await self._client.call_method('canSendGift', {'@type': 'canSendGift', 'gift_id': gift_id})

    async def send_gift(self, gift_id: int = None, owner_id: MessageSender = None, text: formattedText = None, is_private: bool = None, pay_for_upgrade: bool = None) -> Ok:
        """
        description Sends a gift to another user or channel chat. May return an error with a message "STARGIFT_USAGE_LIMITED" if the gift was sold out
        gift_id Identifier of the gift to send
        owner_id Identifier of the user or the channel chat that will receive the gift; limited gifts can't be sent to channel chats
        text Text to show along with the gift; 0-getOption("gift_text_length_max") characters. Only Bold, Italic, Underline, Strikethrough, Spoiler, CustomEmoji, and DateTime entities are allowed.
        is_private Pass true to show gift text and sender only to the gift receiver; otherwise, everyone will be able to see them
        pay_for_upgrade Pass true to additionally pay for the gift upgrade and allow the receiver to upgrade it for free
        """
        return await self._client.call_method('sendGift', {'@type': 'sendGift', 'gift_id': gift_id, 'owner_id': owner_id, 'text': text, 'is_private': is_private, 'pay_for_upgrade': pay_for_upgrade})

    async def get_gift_auction_state(self, auction_id: str = None) -> GiftAuctionState:
        """
        description Returns auction state for a gift @auction_id Unique identifier of the auction
        """
        return await self._client.call_method('getGiftAuctionState', {'@type': 'getGiftAuctionState', 'auction_id': auction_id})

    async def get_gift_auction_acquired_gifts(self, gift_id: int = None) -> GiftAuctionAcquiredGifts:
        """
        description Returns the gifts that were acquired by the current user on a gift auction @gift_id Identifier of the auctioned gift
        """
        return await self._client.call_method('getGiftAuctionAcquiredGifts', {'@type': 'getGiftAuctionAcquiredGifts', 'gift_id': gift_id})

    async def open_gift_auction(self, gift_id: int = None) -> Ok:
        """
        description Informs TDLib that a gift auction was opened by the user @gift_id Identifier of the gift, which auction was opened
        """
        return await self._client.call_method('openGiftAuction', {'@type': 'openGiftAuction', 'gift_id': gift_id})

    async def close_gift_auction(self, gift_id: int = None) -> Ok:
        """
        description Informs TDLib that a gift auction was closed by the user @gift_id Identifier of the gift, which auction was closed
        """
        return await self._client.call_method('closeGiftAuction', {'@type': 'closeGiftAuction', 'gift_id': gift_id})

    async def place_gift_auction_bid(self, gift_id: int = None, star_count: int = None, user_id: int = None, text: formattedText = None, is_private: bool = None) -> Ok:
        """
        description Places a bid on an auction gift
        gift_id Identifier of the gift to place the bid on
        star_count The number of Telegram Stars to place in the bid
        user_id Identifier of the user who will receive the gift
        text Text to show along with the gift; 0-getOption("gift_text_length_max") characters. Only Bold, Italic, Underline, Strikethrough, Spoiler, CustomEmoji, and DateTime entities are allowed.
        is_private Pass true to show gift text and sender only to the gift receiver; otherwise, everyone will be able to see them
        """
        return await self._client.call_method('placeGiftAuctionBid', {'@type': 'placeGiftAuctionBid', 'gift_id': gift_id, 'star_count': star_count, 'user_id': user_id, 'text': text, 'is_private': is_private})

    async def increase_gift_auction_bid(self, gift_id: int = None, star_count: int = None) -> Ok:
        """
        description Increases a bid for an auction gift without changing gift text and receiver
        gift_id Identifier of the gift to put the bid on
        star_count The number of Telegram Stars to put in the bid
        """
        return await self._client.call_method('increaseGiftAuctionBid', {'@type': 'increaseGiftAuctionBid', 'gift_id': gift_id, 'star_count': star_count})

    async def sell_gift(self, business_connection_id: str = None, received_gift_id: str = None) -> Ok:
        """
        description Sells a gift for Telegram Stars; requires owner privileges for gifts owned by a chat
        business_connection_id Unique identifier of business connection on behalf of which to send the request; for bots only
        received_gift_id Identifier of the gift
        """
        return await self._client.call_method('sellGift', {'@type': 'sellGift', 'business_connection_id': business_connection_id, 'received_gift_id': received_gift_id})

    async def toggle_gift_is_saved(self, received_gift_id: str = None, is_saved: bool = None) -> Ok:
        """
        description Toggles whether a gift is shown on the current user's or the channel's profile page; requires can_post_messages administrator right in the channel chat
        received_gift_id Identifier of the gift
        is_saved Pass true to display the gift on the user's or the channel's profile page; pass false to remove it from the profile page
        """
        return await self._client.call_method('toggleGiftIsSaved', {'@type': 'toggleGiftIsSaved', 'received_gift_id': received_gift_id, 'is_saved': is_saved})

    async def set_pinned_gifts(self, owner_id: MessageSender = None, received_gift_ids: List[str] = None) -> Ok:
        """
        description Changes the list of pinned gifts on the current user's or the channel's profile page; requires can_post_messages administrator right in the channel chat
        owner_id Identifier of the user or the channel chat that received the gifts
        received_gift_ids New list of pinned gifts. All gifts must be upgraded and saved on the profile page first. There can be up to getOption("pinned_gift_count_max") pinned gifts
        """
        return await self._client.call_method('setPinnedGifts', {'@type': 'setPinnedGifts', 'owner_id': owner_id, 'received_gift_ids': received_gift_ids})

    async def toggle_chat_gift_notifications(self, chat_id: int = None, are_enabled: bool = None) -> Ok:
        """
        description Toggles whether notifications for new gifts received by a channel chat are sent to the current user; requires can_post_messages administrator right in the chat
        chat_id Identifier of the channel chat
        are_enabled Pass true to enable notifications about new gifts owned by the channel chat; pass false to disable the notifications
        """
        return await self._client.call_method('toggleChatGiftNotifications', {'@type': 'toggleChatGiftNotifications', 'chat_id': chat_id, 'are_enabled': are_enabled})

    async def get_gift_upgrade_preview(self, regular_gift_id: int = None) -> GiftUpgradePreview:
        """
        description Returns examples of possible upgraded gifts for a regular gift @regular_gift_id Identifier of the regular gift
        """
        return await self._client.call_method('getGiftUpgradePreview', {'@type': 'getGiftUpgradePreview', 'regular_gift_id': regular_gift_id})

    async def get_upgraded_gift_variants(self, regular_gift_id: int = None, return_upgrade_models: bool = None, return_craft_models: bool = None) -> GiftUpgradeVariants:
        """
        description Returns all possible variants of upgraded gifts for a regular gift
        regular_gift_id Identifier of the regular gift
        return_upgrade_models Pass true to get models that can be obtained by upgrading a regular gift
        return_craft_models Pass true to get models that can be obtained by crafting a gift from upgraded gifts
        """
        return await self._client.call_method('getUpgradedGiftVariants', {'@type': 'getUpgradedGiftVariants', 'regular_gift_id': regular_gift_id, 'return_upgrade_models': return_upgrade_models, 'return_craft_models': return_craft_models})

    async def upgrade_gift(self, business_connection_id: str = None, received_gift_id: str = None, keep_original_details: bool = None, star_count: int = None) -> UpgradeGiftResult:
        """
        description Upgrades a regular gift
        business_connection_id Unique identifier of business connection on behalf of which to send the request; for bots only
        received_gift_id Identifier of the gift
        keep_original_details Pass true to keep the original gift text, sender and receiver in the upgraded gift
        star_count The Telegram Star amount required to pay for the upgrade. If the gift has prepaid_upgrade_star_count > 0, then pass 0, otherwise, pass gift.upgrade_star_count
        """
        return await self._client.call_method('upgradeGift', {'@type': 'upgradeGift', 'business_connection_id': business_connection_id, 'received_gift_id': received_gift_id, 'keep_original_details': keep_original_details, 'star_count': star_count})

    async def buy_gift_upgrade(self, owner_id: MessageSender = None, prepaid_upgrade_hash: str = None, star_count: int = None) -> Ok:
        """
        description Pays for upgrade of a regular gift that is owned by another user or channel chat
        owner_id Identifier of the user or the channel chat that owns the gift
        prepaid_upgrade_hash Prepaid upgrade hash as received along with the gift
        star_count The Telegram Star amount the user agreed to pay for the upgrade; must be equal to gift.upgrade_star_count
        """
        return await self._client.call_method('buyGiftUpgrade', {'@type': 'buyGiftUpgrade', 'owner_id': owner_id, 'prepaid_upgrade_hash': prepaid_upgrade_hash, 'star_count': star_count})

    async def craft_gift(self, received_gift_ids: List[str] = None) -> CraftGiftResult:
        """
        description Crafts a new gift from other gifts that will be permanently lost
        received_gift_ids Identifier of the gifts to use for crafting. In the case of a successful craft, the resulting gift will have the number of the first gift.
        """
        return await self._client.call_method('craftGift', {'@type': 'craftGift', 'received_gift_ids': received_gift_ids})

    async def transfer_gift(self, business_connection_id: str = None, received_gift_id: str = None, new_owner_id: MessageSender = None, star_count: int = None) -> Ok:
        """
        description Sends an upgraded gift to another user or channel chat
        business_connection_id Unique identifier of business connection on behalf of which to send the request; for bots only
        received_gift_id Identifier of the gift
        new_owner_id Identifier of the user or the channel chat that will receive the gift
        star_count The Telegram Star amount required to pay for the transfer
        """
        return await self._client.call_method('transferGift', {'@type': 'transferGift', 'business_connection_id': business_connection_id, 'received_gift_id': received_gift_id, 'new_owner_id': new_owner_id, 'star_count': star_count})

    async def drop_gift_original_details(self, received_gift_id: str = None, star_count: int = None) -> Ok:
        """
        description Drops original details for an upgraded gift
        received_gift_id Identifier of the gift
        star_count The Telegram Star amount required to pay for the operation
        """
        return await self._client.call_method('dropGiftOriginalDetails', {'@type': 'dropGiftOriginalDetails', 'received_gift_id': received_gift_id, 'star_count': star_count})

    async def send_resold_gift(self, gift_name: str = None, owner_id: MessageSender = None, price: GiftResalePrice = None) -> GiftResaleResult:
        """
        description Sends an upgraded gift that is available for resale to another user or channel chat; gifts already owned by the current user
        gift_name Name of the upgraded gift to send
        owner_id Identifier of the user or the channel chat that will receive the gift
        price The price that the user agreed to pay for the gift
        """
        return await self._client.call_method('sendResoldGift', {'@type': 'sendResoldGift', 'gift_name': gift_name, 'owner_id': owner_id, 'price': price})

    async def send_gift_purchase_offer(self, owner_id: MessageSender = None, gift_name: str = None, price: GiftResalePrice = None, duration: int = None, paid_message_star_count: int = None) -> Ok:
        """
        description Sends an offer to purchase an upgraded gift
        owner_id Identifier of the user or the channel chat that currently owns the gift and will receive the offer
        gift_name Name of the upgraded gift
        price The price that the user agreed to pay for the gift
        duration Duration of the offer, in seconds; must be one of 21600, 43200, 86400, 129600, 172800, or 259200. Can also be 120 if Telegram test environment is used
        paid_message_star_count The number of Telegram Stars the user agreed to pay additionally for sending of the offer message to the current gift owner; pass userFullInfo.outgoing_paid_message_star_count for users and 0 otherwise
        """
        return await self._client.call_method('sendGiftPurchaseOffer', {'@type': 'sendGiftPurchaseOffer', 'owner_id': owner_id, 'gift_name': gift_name, 'price': price, 'duration': duration, 'paid_message_star_count': paid_message_star_count})

    async def process_gift_purchase_offer(self, message_id: int = None, accept: bool = None) -> Ok:
        """
        description Handles a pending gift purchase offer
        message_id Identifier of the message with the gift purchase offer
        accept Pass true to accept the request; pass false to reject it
        """
        return await self._client.call_method('processGiftPurchaseOffer', {'@type': 'processGiftPurchaseOffer', 'message_id': message_id, 'accept': accept})

    async def get_received_gifts(self, business_connection_id: str = None, owner_id: MessageSender = None, collection_id: int = None, exclude_unsaved: bool = None, exclude_saved: bool = None, exclude_unlimited: bool = None, exclude_upgradable: bool = None, exclude_non_upgradable: bool = None, exclude_upgraded: bool = None, exclude_without_colors: bool = None, exclude_hosted: bool = None, sort_by_price: bool = None, offset: str = None, limit: int = None) -> ReceivedGifts:
        """
        description Returns gifts received by the given user or chat
        business_connection_id Unique identifier of business connection on behalf of which to send the request; for bots only
        owner_id Identifier of the gift receiver
        collection_id Pass collection identifier to get gifts only from the specified collection; pass 0 to get gifts regardless of collections
        exclude_unsaved Pass true to exclude gifts that aren't saved to the chat's profile page. Always true for gifts received by other users and channel chats without can_post_messages administrator right
        exclude_saved Pass true to exclude gifts that are saved to the chat's profile page. Always false for gifts received by other users and channel chats without can_post_messages administrator right
        exclude_unlimited Pass true to exclude gifts that can be purchased unlimited number of times
        exclude_upgradable Pass true to exclude gifts that can be purchased limited number of times and can be upgraded
        exclude_non_upgradable Pass true to exclude gifts that can be purchased limited number of times and can't be upgraded
        exclude_upgraded Pass true to exclude upgraded gifts
        exclude_without_colors Pass true to exclude gifts that can't be used in setUpgradedGiftColors
        exclude_hosted Pass true to exclude gifts that are just hosted and are not owned by the owner
        sort_by_price Pass true to sort results by gift price instead of send date
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of gifts to be returned; must be positive and can't be greater than 100. For optimal performance, the number of returned objects is chosen by TDLib and can be smaller than the specified limit
        """
        return await self._client.call_method('getReceivedGifts', {'@type': 'getReceivedGifts', 'business_connection_id': business_connection_id, 'owner_id': owner_id, 'collection_id': collection_id, 'exclude_unsaved': exclude_unsaved, 'exclude_saved': exclude_saved, 'exclude_unlimited': exclude_unlimited, 'exclude_upgradable': exclude_upgradable, 'exclude_non_upgradable': exclude_non_upgradable, 'exclude_upgraded': exclude_upgraded, 'exclude_without_colors': exclude_without_colors, 'exclude_hosted': exclude_hosted, 'sort_by_price': sort_by_price, 'offset': offset, 'limit': limit})

    async def get_received_gift(self, received_gift_id: str = None) -> ReceivedGift:
        """
        description Returns information about a received gift @received_gift_id Identifier of the gift
        """
        return await self._client.call_method('getReceivedGift', {'@type': 'getReceivedGift', 'received_gift_id': received_gift_id})

    async def get_gifts_for_crafting(self, regular_gift_id: int = None, offset: str = None, limit: int = None) -> GiftsForCrafting:
        """
        description Returns upgraded gifts of the current user who can be used to craft another gifts
        regular_gift_id Identifier of the regular gift that will be used for crafting
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of gifts to be returned; must be positive and can't be greater than 100. For optimal performance, the number of returned objects is chosen by TDLib and can be smaller than the specified limit
        """
        return await self._client.call_method('getGiftsForCrafting', {'@type': 'getGiftsForCrafting', 'regular_gift_id': regular_gift_id, 'offset': offset, 'limit': limit})

    async def get_upgraded_gift(self, name: str = None) -> UpgradedGift:
        """
        description Returns information about an upgraded gift by its name @name Unique name of the upgraded gift
        """
        return await self._client.call_method('getUpgradedGift', {'@type': 'getUpgradedGift', 'name': name})

    async def get_upgraded_gift_value_info(self, name: str = None) -> UpgradedGiftValueInfo:
        """
        description Returns information about value of an upgraded gift by its name @name Unique name of the upgraded gift
        """
        return await self._client.call_method('getUpgradedGiftValueInfo', {'@type': 'getUpgradedGiftValueInfo', 'name': name})

    async def get_upgraded_gift_withdrawal_url(self, received_gift_id: str = None, password: str = None) -> HttpUrl:
        """
        description Returns a URL for upgraded gift withdrawal in the TON blockchain as an NFT; requires owner privileges for gifts owned by a chat
        received_gift_id Identifier of the gift
        password The 2-step verification password of the current user
        """
        return await self._client.call_method('getUpgradedGiftWithdrawalUrl', {'@type': 'getUpgradedGiftWithdrawalUrl', 'received_gift_id': received_gift_id, 'password': password})

    async def get_upgraded_gifts_promotional_animation(self) -> Animation:
        """
        description Returns promotional animation for upgraded gifts
        """
        return await self._client.call_method('getUpgradedGiftsPromotionalAnimation', {'@type': 'getUpgradedGiftsPromotionalAnimation'})

    async def set_gift_resale_price(self, received_gift_id: str = None, price: GiftResalePrice = None) -> Ok:
        """
        description Changes resale price of a unique gift owned by the current user
        received_gift_id Identifier of the unique gift
        price The new price for the unique gift; pass null to disallow gift resale. The current user will receive
        """
        return await self._client.call_method('setGiftResalePrice', {'@type': 'setGiftResalePrice', 'received_gift_id': received_gift_id, 'price': price})

    async def search_gifts_for_resale(self, gift_id: int = None, order: GiftForResaleOrder = None, for_crafting: bool = None, for_stars: bool = None, attributes: List[UpgradedGiftAttributeId] = None, offset: str = None, limit: int = None) -> GiftsForResale:
        """
        description Returns upgraded gifts that can be bought from other owners using sendResoldGift
        gift_id Identifier of the regular gift that was upgraded to a unique gift
        order Order in which the results will be sorted
        for_crafting Pass true to get only gifts suitable for crafting
        for_stars Pass true to get only gifts that can be bought using Telegram Stars
        attributes Attributes used to filter received gifts. If multiple attributes of the same type are specified, then all of them are allowed.
        offset Offset of the first entry to return as received from the previous request with the same order and attributes; use empty string to get the first chunk of results
        limit The maximum number of gifts to return
        """
        return await self._client.call_method('searchGiftsForResale', {'@type': 'searchGiftsForResale', 'gift_id': gift_id, 'order': order, 'for_crafting': for_crafting, 'for_stars': for_stars, 'attributes': attributes, 'offset': offset, 'limit': limit})

    async def get_gift_collections(self, owner_id: MessageSender = None) -> GiftCollections:
        """
        description Returns collections of gifts owned by the given user or chat
        owner_id Identifier of the user or the channel chat that received the gifts
        """
        return await self._client.call_method('getGiftCollections', {'@type': 'getGiftCollections', 'owner_id': owner_id})

    async def create_gift_collection(self, owner_id: MessageSender = None, name: str = None, received_gift_ids: List[str] = None) -> GiftCollection:
        """
        description Creates a collection from gifts on the current user's or a channel's profile page; requires can_post_messages administrator right in the channel chat.
        owner_id Identifier of the user or the channel chat that received the gifts
        name Name of the collection; 1-12 characters
        received_gift_ids Identifier of the gifts to add to the collection; 0-getOption("gift_collection_size_max") identifiers
        """
        return await self._client.call_method('createGiftCollection', {'@type': 'createGiftCollection', 'owner_id': owner_id, 'name': name, 'received_gift_ids': received_gift_ids})

    async def reorder_gift_collections(self, owner_id: MessageSender = None, collection_ids: List[int] = None) -> Ok:
        """
        description Changes order of gift collections. If the collections are owned by a channel chat, then requires can_post_messages administrator right in the channel chat
        owner_id Identifier of the user or the channel chat that owns the collection
        collection_ids New order of gift collections
        """
        return await self._client.call_method('reorderGiftCollections', {'@type': 'reorderGiftCollections', 'owner_id': owner_id, 'collection_ids': collection_ids})

    async def delete_gift_collection(self, owner_id: MessageSender = None, collection_id: int = None) -> Ok:
        """
        description Deletes a gift collection. If the collection is owned by a channel chat, then requires can_post_messages administrator right in the channel chat
        owner_id Identifier of the user or the channel chat that owns the collection
        collection_id Identifier of the gift collection
        """
        return await self._client.call_method('deleteGiftCollection', {'@type': 'deleteGiftCollection', 'owner_id': owner_id, 'collection_id': collection_id})

    async def set_gift_collection_name(self, owner_id: MessageSender = None, collection_id: int = None, name: str = None) -> GiftCollection:
        """
        description Changes name of a gift collection. If the collection is owned by a channel chat, then requires can_post_messages administrator right in the channel chat. Returns the changed collection
        owner_id Identifier of the user or the channel chat that owns the collection
        collection_id Identifier of the gift collection
        name New name of the collection; 1-12 characters
        """
        return await self._client.call_method('setGiftCollectionName', {'@type': 'setGiftCollectionName', 'owner_id': owner_id, 'collection_id': collection_id, 'name': name})

    async def add_gift_collection_gifts(self, owner_id: MessageSender = None, collection_id: int = None, received_gift_ids: List[str] = None) -> GiftCollection:
        """
        description Adds gifts to the beginning of a previously created collection. If the collection is owned by a channel chat, then requires can_post_messages administrator right in the channel chat. Returns the changed collection
        owner_id Identifier of the user or the channel chat that owns the collection
        collection_id Identifier of the gift collection
        received_gift_ids Identifier of the gifts to add to the collection; 1-getOption("gift_collection_size_max") identifiers.
        """
        return await self._client.call_method('addGiftCollectionGifts', {'@type': 'addGiftCollectionGifts', 'owner_id': owner_id, 'collection_id': collection_id, 'received_gift_ids': received_gift_ids})

    async def remove_gift_collection_gifts(self, owner_id: MessageSender = None, collection_id: int = None, received_gift_ids: List[str] = None) -> GiftCollection:
        """
        description Removes gifts from a collection. If the collection is owned by a channel chat, then requires can_post_messages administrator right in the channel chat. Returns the changed collection
        owner_id Identifier of the user or the channel chat that owns the collection
        collection_id Identifier of the gift collection
        received_gift_ids Identifier of the gifts to remove from the collection
        """
        return await self._client.call_method('removeGiftCollectionGifts', {'@type': 'removeGiftCollectionGifts', 'owner_id': owner_id, 'collection_id': collection_id, 'received_gift_ids': received_gift_ids})

    async def reorder_gift_collection_gifts(self, owner_id: MessageSender = None, collection_id: int = None, received_gift_ids: List[str] = None) -> GiftCollection:
        """
        description Changes order of gifts in a collection. If the collection is owned by a channel chat, then requires can_post_messages administrator right in the channel chat. Returns the changed collection
        owner_id Identifier of the user or the channel chat that owns the collection
        collection_id Identifier of the gift collection
        received_gift_ids Identifier of the gifts to move to the beginning of the collection. All other gifts are placed in the current order after the specified gifts
        """
        return await self._client.call_method('reorderGiftCollectionGifts', {'@type': 'reorderGiftCollectionGifts', 'owner_id': owner_id, 'collection_id': collection_id, 'received_gift_ids': received_gift_ids})

    async def create_invoice_link(self, business_connection_id: str = None, invoice: InputMessageContent = None) -> HttpUrl:
        """
        description Creates a link for the given invoice; for bots only
        business_connection_id Unique identifier of business connection on behalf of which to send the request
        invoice Information about the invoice of the type inputMessageInvoice
        """
        return await self._client.call_method('createInvoiceLink', {'@type': 'createInvoiceLink', 'business_connection_id': business_connection_id, 'invoice': invoice})

    async def refund_star_payment(self, user_id: int = None, telegram_payment_charge_id: str = None) -> Ok:
        """
        description Refunds a previously done payment in Telegram Stars; for bots only
        user_id Identifier of the user who did the payment
        telegram_payment_charge_id Telegram payment identifier
        """
        return await self._client.call_method('refundStarPayment', {'@type': 'refundStarPayment', 'user_id': user_id, 'telegram_payment_charge_id': telegram_payment_charge_id})

    async def get_support_user(self) -> User:
        """
        description Returns a user who can be contacted to get support
        """
        return await self._client.call_method('getSupportUser', {'@type': 'getSupportUser'})

    async def get_background_url(self, name: str = None, type: BackgroundType = None) -> HttpUrl:
        """
        description Constructs a persistent HTTP URL for a background @name Background name @type Background type; backgroundTypeChatTheme isn't supported
        """
        return await self._client.call_method('getBackgroundUrl', {'@type': 'getBackgroundUrl', 'name': name, 'type': type})

    async def search_background(self, name: str = None) -> Background:
        """
        description Searches for a background by its name @name The name of the background
        """
        return await self._client.call_method('searchBackground', {'@type': 'searchBackground', 'name': name})

    async def set_default_background(self, background: InputBackground = None, type: BackgroundType = None, for_dark_theme: bool = None) -> Background:
        """
        description Sets default background for chats; adds the background to the list of installed backgrounds
        background The input background to use; pass null to create a new filled background
        type Background type; pass null to use the default type of the remote background; backgroundTypeChatTheme isn't supported
        for_dark_theme Pass true if the background is set for a dark theme
        """
        return await self._client.call_method('setDefaultBackground', {'@type': 'setDefaultBackground', 'background': background, 'type': type, 'for_dark_theme': for_dark_theme})

    async def delete_default_background(self, for_dark_theme: bool = None) -> Ok:
        """
        description Deletes default background for chats @for_dark_theme Pass true if the background is deleted for a dark theme
        """
        return await self._client.call_method('deleteDefaultBackground', {'@type': 'deleteDefaultBackground', 'for_dark_theme': for_dark_theme})

    async def get_installed_backgrounds(self, for_dark_theme: bool = None) -> Backgrounds:
        """
        description Returns backgrounds installed by the user @for_dark_theme Pass true to order returned backgrounds for a dark theme
        """
        return await self._client.call_method('getInstalledBackgrounds', {'@type': 'getInstalledBackgrounds', 'for_dark_theme': for_dark_theme})

    async def remove_installed_background(self, background_id: int = None) -> Ok:
        """
        description Removes background from the list of installed backgrounds @background_id The background identifier
        """
        return await self._client.call_method('removeInstalledBackground', {'@type': 'removeInstalledBackground', 'background_id': background_id})

    async def reset_installed_backgrounds(self) -> Ok:
        """
        description Resets list of installed backgrounds to its default value
        """
        return await self._client.call_method('resetInstalledBackgrounds', {'@type': 'resetInstalledBackgrounds'})

    async def get_localization_target_info(self, only_local: bool = None) -> LocalizationTargetInfo:
        """
        description Returns information about the current localization target. This is an offline method if only_local is true. Can be called before authorization @only_local Pass true to get only locally available information without sending network requests
        """
        return await self._client.call_method('getLocalizationTargetInfo', {'@type': 'getLocalizationTargetInfo', 'only_local': only_local})

    async def get_language_pack_info(self, language_pack_id: str = None) -> LanguagePackInfo:
        """
        description Returns information about a language pack. Returned language pack identifier may be different from a provided one. Can be called before authorization @language_pack_id Language pack identifier
        """
        return await self._client.call_method('getLanguagePackInfo', {'@type': 'getLanguagePackInfo', 'language_pack_id': language_pack_id})

    async def get_language_pack_strings(self, language_pack_id: str = None, keys: List[str] = None) -> LanguagePackStrings:
        """
        description Returns strings from a language pack in the current localization target by their keys. Can be called before authorization
        language_pack_id Language pack identifier of the strings to be returned
        keys Language pack keys of the strings to be returned; leave empty to request all available strings
        """
        return await self._client.call_method('getLanguagePackStrings', {'@type': 'getLanguagePackStrings', 'language_pack_id': language_pack_id, 'keys': keys})

    async def synchronize_language_pack(self, language_pack_id: str = None) -> Ok:
        """
        description Fetches the latest versions of all strings from a language pack in the current localization target from the server.
        language_pack_id Language pack identifier
        """
        return await self._client.call_method('synchronizeLanguagePack', {'@type': 'synchronizeLanguagePack', 'language_pack_id': language_pack_id})

    async def add_custom_server_language_pack(self, language_pack_id: str = None) -> Ok:
        """
        description Adds a custom server language pack to the list of installed language packs in current localization target. Can be called before authorization @language_pack_id Identifier of a language pack to be added
        """
        return await self._client.call_method('addCustomServerLanguagePack', {'@type': 'addCustomServerLanguagePack', 'language_pack_id': language_pack_id})

    async def set_custom_language_pack(self, info: languagePackInfo = None, strings: List[languagePackString] = None) -> Ok:
        """
        description Adds or changes a custom local language pack to the current localization target
        info Information about the language pack. Language pack identifier must start with 'X', consist only of English letters, digits and hyphens, and must not exceed 64 characters. Can be called before authorization
        strings Strings of the new language pack
        """
        return await self._client.call_method('setCustomLanguagePack', {'@type': 'setCustomLanguagePack', 'info': info, 'strings': strings})

    async def edit_custom_language_pack_info(self, info: languagePackInfo = None) -> Ok:
        """
        description Edits information about a custom local language pack in the current localization target. Can be called before authorization @info New information about the custom local language pack
        """
        return await self._client.call_method('editCustomLanguagePackInfo', {'@type': 'editCustomLanguagePackInfo', 'info': info})

    async def set_custom_language_pack_string(self, language_pack_id: str = None, new_string: languagePackString = None) -> Ok:
        """
        description Adds, edits or deletes a string in a custom local language pack. Can be called before authorization @language_pack_id Identifier of a previously added custom local language pack in the current localization target @new_string New language pack string
        """
        return await self._client.call_method('setCustomLanguagePackString', {'@type': 'setCustomLanguagePackString', 'language_pack_id': language_pack_id, 'new_string': new_string})

    async def delete_language_pack(self, language_pack_id: str = None) -> Ok:
        """
        description Deletes all information about a language pack in the current localization target. The language pack which is currently in use (including base language pack) or is being synchronized can't be deleted.
        language_pack_id Identifier of the language pack to delete
        """
        return await self._client.call_method('deleteLanguagePack', {'@type': 'deleteLanguagePack', 'language_pack_id': language_pack_id})

    async def register_device(self, device_token: DeviceToken = None, other_user_ids: List[int] = None) -> PushReceiverId:
        """
        description Registers the currently used device for receiving push notifications. Returns a globally unique identifier of the push notification subscription @device_token Device token @other_user_ids List of user identifiers of other users currently using the application
        """
        return await self._client.call_method('registerDevice', {'@type': 'registerDevice', 'device_token': device_token, 'other_user_ids': other_user_ids})

    async def process_push_notification(self, payload: str = None) -> Ok:
        """
        description Handles a push notification. Returns error with code 406 if the push notification is not supported and connection to the server is required to fetch new data. Can be called before authorization
        payload JSON-encoded push notification payload with all fields sent by the server, and "google.sent_time" and "google.notification.sound" fields added
        """
        return await self._client.call_method('processPushNotification', {'@type': 'processPushNotification', 'payload': payload})

    async def get_push_receiver_id(self, payload: str = None) -> PushReceiverId:
        """
        description Returns a globally unique push notification subscription identifier for identification of an account, which has received a push notification. Can be called synchronously @payload JSON-encoded push notification payload
        """
        return await self._client.call_method('getPushReceiverId', {'@type': 'getPushReceiverId', 'payload': payload})

    async def get_recently_visited_t_me_urls(self, referrer: str = None) -> TMeUrls:
        """
        description Returns t.me URLs recently visited by a newly registered user @referrer Google Play referrer to identify the user
        """
        return await self._client.call_method('getRecentlyVisitedTMeUrls', {'@type': 'getRecentlyVisitedTMeUrls', 'referrer': referrer})

    async def set_user_privacy_setting_rules(self, setting: UserPrivacySetting = None, rules: userPrivacySettingRules = None) -> Ok:
        """
        description Changes user privacy settings @setting The privacy setting @rules The new privacy rules
        """
        return await self._client.call_method('setUserPrivacySettingRules', {'@type': 'setUserPrivacySettingRules', 'setting': setting, 'rules': rules})

    async def get_user_privacy_setting_rules(self, setting: UserPrivacySetting = None) -> UserPrivacySettingRules:
        """
        description Returns the current privacy settings @setting The privacy setting
        """
        return await self._client.call_method('getUserPrivacySettingRules', {'@type': 'getUserPrivacySettingRules', 'setting': setting})

    async def set_read_date_privacy_settings(self, settings: readDatePrivacySettings = None) -> Ok:
        """
        description Changes privacy settings for message read date @settings New settings
        """
        return await self._client.call_method('setReadDatePrivacySettings', {'@type': 'setReadDatePrivacySettings', 'settings': settings})

    async def get_read_date_privacy_settings(self) -> ReadDatePrivacySettings:
        """
        description Returns privacy settings for message read date
        """
        return await self._client.call_method('getReadDatePrivacySettings', {'@type': 'getReadDatePrivacySettings'})

    async def set_new_chat_privacy_settings(self, settings: newChatPrivacySettings = None) -> Ok:
        """
        description Changes privacy settings for new chat creation; can be used only if getOption("can_set_new_chat_privacy_settings") @settings New settings
        """
        return await self._client.call_method('setNewChatPrivacySettings', {'@type': 'setNewChatPrivacySettings', 'settings': settings})

    async def get_new_chat_privacy_settings(self) -> NewChatPrivacySettings:
        """
        description Returns privacy settings for new chat creation
        """
        return await self._client.call_method('getNewChatPrivacySettings', {'@type': 'getNewChatPrivacySettings'})

    async def get_paid_message_revenue(self, user_id: int = None) -> StarCount:
        """
        description Returns the total number of Telegram Stars received by the current user for paid messages from the given user @user_id Identifier of the user
        """
        return await self._client.call_method('getPaidMessageRevenue', {'@type': 'getPaidMessageRevenue', 'user_id': user_id})

    async def allow_unpaid_messages_from_user(self, user_id: int = None, refund_payments: bool = None) -> Ok:
        """
        description Allows the specified user to send unpaid private messages to the current user by adding a rule to userPrivacySettingAllowUnpaidMessages
        user_id Identifier of the user
        refund_payments Pass true to refund the user previously paid messages
        """
        return await self._client.call_method('allowUnpaidMessagesFromUser', {'@type': 'allowUnpaidMessagesFromUser', 'user_id': user_id, 'refund_payments': refund_payments})

    async def set_chat_paid_message_star_count(self, chat_id: int = None, paid_message_star_count: int = None) -> Ok:
        """
        description Changes the Telegram Star amount that must be paid to send a message to a supergroup chat; requires can_restrict_members administrator right and supergroupFullInfo.can_enable_paid_messages
        chat_id Identifier of the supergroup chat
        paid_message_star_count The new number of Telegram Stars that must be paid for each message that is sent to the supergroup chat unless the sender is an administrator of the chat; 0-getOption("paid_message_star_count_max").
        """
        return await self._client.call_method('setChatPaidMessageStarCount', {'@type': 'setChatPaidMessageStarCount', 'chat_id': chat_id, 'paid_message_star_count': paid_message_star_count})

    async def can_send_message_to_user(self, user_id: int = None, only_local: bool = None) -> CanSendMessageToUserResult:
        """
        description Checks whether the current user can message another user or try to create a chat with them
        user_id Identifier of the other user
        only_local Pass true to get only locally available information without sending network requests
        """
        return await self._client.call_method('canSendMessageToUser', {'@type': 'canSendMessageToUser', 'user_id': user_id, 'only_local': only_local})

    async def get_option(self, name: str = None) -> OptionValue:
        """
        description Returns the value of an option by its name. (Check the list of available options on https://core.telegram.org/tdlib/options.) Can be called before authorization. Can be called synchronously for options "version" and "commit_hash"
        name The name of the option
        """
        return await self._client.call_method('getOption', {'@type': 'getOption', 'name': name})

    async def set_option(self, name: str = None, value: OptionValue = None) -> Ok:
        """
        description Sets the value of an option. (Check the list of available options on https://core.telegram.org/tdlib/options.) Only writable options can be set. Can be called before authorization
        name The name of the option
        value The new value of the option; pass null to reset option value to a default value
        """
        return await self._client.call_method('setOption', {'@type': 'setOption', 'name': name, 'value': value})

    async def set_account_ttl(self, ttl: accountTtl = None) -> Ok:
        """
        description Changes the period of inactivity after which the account of the current user will automatically be deleted @ttl New account TTL
        """
        return await self._client.call_method('setAccountTtl', {'@type': 'setAccountTtl', 'ttl': ttl})

    async def get_account_ttl(self) -> AccountTtl:
        """
        description Returns the period of inactivity after which the account of the current user will automatically be deleted
        """
        return await self._client.call_method('getAccountTtl', {'@type': 'getAccountTtl'})

    async def delete_account(self, reason: str = None, password: str = None) -> Ok:
        """
        description Deletes the account of the current user, deleting all information associated with the user from the server. The phone number of the account can be used to create a new account.
        reason The reason why the account was deleted; optional
        password The 2-step verification password of the current user. If the current user isn't authorized, then an empty string can be passed and account deletion can be canceled within one week
        """
        return await self._client.call_method('deleteAccount', {'@type': 'deleteAccount', 'reason': reason, 'password': password})

    async def set_default_message_auto_delete_time(self, message_auto_delete_time: messageAutoDeleteTime = None) -> Ok:
        """
        description Changes the default message auto-delete time for new chats @message_auto_delete_time New default message auto-delete time; must be from 0 up to 365 * 86400 and be divisible by 86400. If 0, then messages aren't deleted automatically
        """
        return await self._client.call_method('setDefaultMessageAutoDeleteTime', {'@type': 'setDefaultMessageAutoDeleteTime', 'message_auto_delete_time': message_auto_delete_time})

    async def get_default_message_auto_delete_time(self) -> MessageAutoDeleteTime:
        """
        description Returns default message auto-delete time setting for new chats
        """
        return await self._client.call_method('getDefaultMessageAutoDeleteTime', {'@type': 'getDefaultMessageAutoDeleteTime'})

    async def remove_chat_action_bar(self, chat_id: int = None) -> Ok:
        """
        description Removes a chat action bar without any other action @chat_id Chat identifier
        """
        return await self._client.call_method('removeChatActionBar', {'@type': 'removeChatActionBar', 'chat_id': chat_id})

    async def report_chat(self, chat_id: int = None, option_id: bytes = None, message_ids: List[int] = None, text: str = None) -> ReportChatResult:
        """
        description Reports a chat to the Telegram moderators. A chat can be reported only from the chat action bar, or if chat.can_be_reported
        chat_id Chat identifier
        option_id Option identifier chosen by the user; leave empty for the initial request
        message_ids Identifiers of reported messages. Use messageProperties.can_report_chat to check whether the message can be reported
        text Additional report details if asked by the server; 0-1024 characters; leave empty for the initial request
        """
        return await self._client.call_method('reportChat', {'@type': 'reportChat', 'chat_id': chat_id, 'option_id': option_id, 'message_ids': message_ids, 'text': text})

    async def report_chat_photo(self, chat_id: int = None, file_id: int = None, reason: ReportReason = None, text: str = None) -> Ok:
        """
        description Reports a chat photo to the Telegram moderators. A chat photo can be reported only if chat.can_be_reported
        chat_id Chat identifier
        file_id Identifier of the photo to report. Only full photos from chatPhoto can be reported
        reason The reason for reporting the chat photo
        text Additional report details; 0-1024 characters
        """
        return await self._client.call_method('reportChatPhoto', {'@type': 'reportChatPhoto', 'chat_id': chat_id, 'file_id': file_id, 'reason': reason, 'text': text})

    async def report_message_reactions(self, chat_id: int = None, message_id: int = None, sender_id: MessageSender = None) -> Ok:
        """
        description Reports reactions set on a message to the Telegram moderators. Reactions on a message can be reported only if messageProperties.can_report_reactions
        chat_id Chat identifier
        message_id Message identifier
        sender_id Identifier of the sender, which added the reaction
        """
        return await self._client.call_method('reportMessageReactions', {'@type': 'reportMessageReactions', 'chat_id': chat_id, 'message_id': message_id, 'sender_id': sender_id})

    async def get_chat_revenue_statistics(self, chat_id: int = None, is_dark: bool = None) -> ChatRevenueStatistics:
        """
        description Returns detailed revenue statistics about a chat. Currently, this method can be used only
        chat_id Chat identifier
        is_dark Pass true if a dark theme is used by the application
        """
        return await self._client.call_method('getChatRevenueStatistics', {'@type': 'getChatRevenueStatistics', 'chat_id': chat_id, 'is_dark': is_dark})

    async def get_chat_revenue_withdrawal_url(self, chat_id: int = None, password: str = None) -> HttpUrl:
        """
        description Returns a URL for chat revenue withdrawal; requires owner privileges in the channel chat or the bot. Currently, this method can be used only
        chat_id Chat identifier
        password The 2-step verification password of the current user
        """
        return await self._client.call_method('getChatRevenueWithdrawalUrl', {'@type': 'getChatRevenueWithdrawalUrl', 'chat_id': chat_id, 'password': password})

    async def get_chat_revenue_transactions(self, chat_id: int = None, offset: str = None, limit: int = None) -> ChatRevenueTransactions:
        """
        description Returns the list of revenue transactions for a chat. Currently, this method can be used only
        chat_id Chat identifier
        offset Offset of the first transaction to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of transactions to be returned; up to 100
        """
        return await self._client.call_method('getChatRevenueTransactions', {'@type': 'getChatRevenueTransactions', 'chat_id': chat_id, 'offset': offset, 'limit': limit})

    async def get_ton_transactions(self, direction: TransactionDirection = None, offset: str = None, limit: int = None) -> TonTransactions:
        """
        description Returns the list of Toncoin transactions of the current user
        direction Direction of the transactions to receive; pass null to get all transactions
        offset Offset of the first transaction to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of transactions to return
        """
        return await self._client.call_method('getTonTransactions', {'@type': 'getTonTransactions', 'direction': direction, 'offset': offset, 'limit': limit})

    async def get_star_revenue_statistics(self, owner_id: MessageSender = None, is_dark: bool = None) -> StarRevenueStatistics:
        """
        description Returns detailed Telegram Star revenue statistics
        owner_id Identifier of the owner of the Telegram Stars; can be identifier of the current user, an owned bot, or a supergroup or a channel chat with supergroupFullInfo.can_get_star_revenue_statistics == true
        is_dark Pass true if a dark theme is used by the application
        """
        return await self._client.call_method('getStarRevenueStatistics', {'@type': 'getStarRevenueStatistics', 'owner_id': owner_id, 'is_dark': is_dark})

    async def get_star_withdrawal_url(self, owner_id: MessageSender = None, star_count: int = None, password: str = None) -> HttpUrl:
        """
        description Returns a URL for Telegram Star withdrawal
        owner_id Identifier of the owner of the Telegram Stars; can be identifier of the current user, an owned bot, or an owned supergroup or channel chat
        star_count The number of Telegram Stars to withdraw; must be between getOption("star_withdrawal_count_min") and getOption("star_withdrawal_count_max")
        password The 2-step verification password of the current user
        """
        return await self._client.call_method('getStarWithdrawalUrl', {'@type': 'getStarWithdrawalUrl', 'owner_id': owner_id, 'star_count': star_count, 'password': password})

    async def get_star_ad_account_url(self, owner_id: MessageSender = None) -> HttpUrl:
        """
        description Returns a URL for a Telegram Ad platform account that can be used to set up advertisements for the chat paid in the owned Telegram Stars
        owner_id Identifier of the owner of the Telegram Stars; can be identifier of an owned bot, or identifier of an owned channel chat
        """
        return await self._client.call_method('getStarAdAccountUrl', {'@type': 'getStarAdAccountUrl', 'owner_id': owner_id})

    async def get_ton_revenue_statistics(self, is_dark: bool = None) -> TonRevenueStatistics:
        """
        description Returns detailed Toncoin revenue statistics of the current user @is_dark Pass true if a dark theme is used by the application
        """
        return await self._client.call_method('getTonRevenueStatistics', {'@type': 'getTonRevenueStatistics', 'is_dark': is_dark})

    async def get_ton_withdrawal_url(self, password: str = None) -> HttpUrl:
        """
        description Returns a URL for Toncoin withdrawal from the current user's account. The user must have at least 10 toncoins to withdraw
        password The 2-step verification password of the current user
        """
        return await self._client.call_method('getTonWithdrawalUrl', {'@type': 'getTonWithdrawalUrl', 'password': password})

    async def get_chat_statistics(self, chat_id: int = None, is_dark: bool = None) -> ChatStatistics:
        """
        description Returns detailed statistics about a chat. Currently, this method can be used only for supergroups and channels. Can be used only if supergroupFullInfo.can_get_statistics == true @chat_id Chat identifier @is_dark Pass true if a dark theme is used by the application
        """
        return await self._client.call_method('getChatStatistics', {'@type': 'getChatStatistics', 'chat_id': chat_id, 'is_dark': is_dark})

    async def get_message_statistics(self, chat_id: int = None, message_id: int = None, is_dark: bool = None) -> MessageStatistics:
        """
        description Returns detailed statistics about a message. Can be used only if messageProperties.can_get_statistics == true @chat_id Chat identifier @message_id Message identifier @is_dark Pass true if a dark theme is used by the application
        """
        return await self._client.call_method('getMessageStatistics', {'@type': 'getMessageStatistics', 'chat_id': chat_id, 'message_id': message_id, 'is_dark': is_dark})

    async def get_message_public_forwards(self, chat_id: int = None, message_id: int = None, offset: str = None, limit: int = None) -> PublicForwards:
        """
        description Returns forwarded copies of a channel message to different public channels and public reposts as a story. Can be used only if messageProperties.can_get_statistics == true. For optimal performance, the number of returned messages and stories is chosen by TDLib
        chat_id Chat identifier of the message
        message_id Message identifier
        offset Offset of the first entry to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of messages and stories to be returned; must be positive and can't be greater than 100. For optimal performance, the number of returned objects is chosen by TDLib and can be smaller than the specified limit
        """
        return await self._client.call_method('getMessagePublicForwards', {'@type': 'getMessagePublicForwards', 'chat_id': chat_id, 'message_id': message_id, 'offset': offset, 'limit': limit})

    async def get_story_statistics(self, chat_id: int = None, story_id: int = None, is_dark: bool = None) -> StoryStatistics:
        """
        description Returns detailed statistics about a story. Can be used only if story.can_get_statistics == true @chat_id Chat identifier @story_id Story identifier @is_dark Pass true if a dark theme is used by the application
        """
        return await self._client.call_method('getStoryStatistics', {'@type': 'getStoryStatistics', 'chat_id': chat_id, 'story_id': story_id, 'is_dark': is_dark})

    async def get_statistical_graph(self, chat_id: int = None, token: str = None, x: int = None) -> StatisticalGraph:
        """
        description Loads an asynchronous or a zoomed in statistical graph @chat_id Chat identifier @token The token for graph loading @x X-value for zoomed in graph or 0 otherwise
        """
        return await self._client.call_method('getStatisticalGraph', {'@type': 'getStatisticalGraph', 'chat_id': chat_id, 'token': token, 'x': x})

    async def get_storage_statistics(self, chat_limit: int = None) -> StorageStatistics:
        """
        description Returns storage usage statistics. Can be called before authorization
        chat_limit The maximum number of chats with the largest storage usage for which separate statistics need to be returned. All other chats will be grouped in entries with chat_id == 0. If the chat info database is not used, the chat_limit is ignored and is always set to 0
        """
        return await self._client.call_method('getStorageStatistics', {'@type': 'getStorageStatistics', 'chat_limit': chat_limit})

    async def get_storage_statistics_fast(self) -> StorageStatisticsFast:
        """
        description Quickly returns approximate storage usage statistics. Can be called before authorization
        """
        return await self._client.call_method('getStorageStatisticsFast', {'@type': 'getStorageStatisticsFast'})

    async def get_database_statistics(self) -> DatabaseStatistics:
        """
        description Returns database statistics
        """
        return await self._client.call_method('getDatabaseStatistics', {'@type': 'getDatabaseStatistics'})

    async def optimize_storage(self, size: int = None, ttl: int = None, count: int = None, immunity_delay: int = None, file_types: List[FileType] = None, chat_ids: List[int] = None, exclude_chat_ids: List[int] = None, return_deleted_file_statistics: bool = None, chat_limit: int = None) -> StorageStatistics:
        """
        description Optimizes storage usage, i.e. deletes some files and returns new storage usage statistics. Secret thumbnails can't be deleted
        size Limit on the total size of files after deletion, in bytes. Pass -1 to use the default limit
        ttl Limit on the time that has passed since the last time a file was accessed (or creation time for some filesystems). Pass -1 to use the default limit
        count Limit on the total number of files after deletion. Pass -1 to use the default limit
        immunity_delay The amount of time after the creation of a file during which it can't be deleted, in seconds. Pass -1 to use the default value
        file_types If non-empty, only files with the given types are considered. By default, all types except thumbnails, profile photos, stickers and wallpapers are deleted
        chat_ids If non-empty, only files from the given chats are considered. Use 0 as chat identifier to delete files not belonging to any chat (e.g., profile photos)
        exclude_chat_ids If non-empty, files from the given chats are excluded. Use 0 as chat identifier to exclude all files not belonging to any chat (e.g., profile photos)
        return_deleted_file_statistics Pass true if statistics about the files that were deleted must be returned instead of the whole storage usage statistics. Affects only returned statistics
        chat_limit Same as in getStorageStatistics. Affects only returned statistics
        """
        return await self._client.call_method('optimizeStorage', {'@type': 'optimizeStorage', 'size': size, 'ttl': ttl, 'count': count, 'immunity_delay': immunity_delay, 'file_types': file_types, 'chat_ids': chat_ids, 'exclude_chat_ids': exclude_chat_ids, 'return_deleted_file_statistics': return_deleted_file_statistics, 'chat_limit': chat_limit})

    async def set_network_type(self, type: NetworkType = None) -> Ok:
        """
        description Sets the current network type. Can be called before authorization. Calling this method forces all network connections to reopen, mitigating the delay in switching between different networks,
        type The new network type; pass null to set network type to networkTypeOther
        """
        return await self._client.call_method('setNetworkType', {'@type': 'setNetworkType', 'type': type})

    async def get_network_statistics(self, only_current: bool = None) -> NetworkStatistics:
        """
        description Returns network data usage statistics. Can be called before authorization @only_current Pass true to get statistics only for the current library launch
        """
        return await self._client.call_method('getNetworkStatistics', {'@type': 'getNetworkStatistics', 'only_current': only_current})

    async def add_network_statistics(self, entry: NetworkStatisticsEntry = None) -> Ok:
        """
        description Adds the specified data to data usage statistics. Can be called before authorization @entry The network statistics entry with the data to be added to statistics
        """
        return await self._client.call_method('addNetworkStatistics', {'@type': 'addNetworkStatistics', 'entry': entry})

    async def reset_network_statistics(self) -> Ok:
        """
        description Resets all network data usage statistics to zero. Can be called before authorization
        """
        return await self._client.call_method('resetNetworkStatistics', {'@type': 'resetNetworkStatistics'})

    async def get_auto_download_settings_presets(self) -> AutoDownloadSettingsPresets:
        """
        description Returns auto-download settings presets for the current user
        """
        return await self._client.call_method('getAutoDownloadSettingsPresets', {'@type': 'getAutoDownloadSettingsPresets'})

    async def set_auto_download_settings(self, settings: autoDownloadSettings = None, type: NetworkType = None) -> Ok:
        """
        description Sets auto-download settings @settings New user auto-download settings @type Type of the network for which the new settings are relevant
        """
        return await self._client.call_method('setAutoDownloadSettings', {'@type': 'setAutoDownloadSettings', 'settings': settings, 'type': type})

    async def get_autosave_settings(self) -> AutosaveSettings:
        """
        description Returns autosave settings for the current user
        """
        return await self._client.call_method('getAutosaveSettings', {'@type': 'getAutosaveSettings'})

    async def set_autosave_settings(self, scope: AutosaveSettingsScope = None, settings: scopeAutosaveSettings = None) -> Ok:
        """
        description Sets autosave settings for the given scope. The method is guaranteed to work only after at least one call to getAutosaveSettings @scope Autosave settings scope @settings New autosave settings for the scope; pass null to set autosave settings to default
        """
        return await self._client.call_method('setAutosaveSettings', {'@type': 'setAutosaveSettings', 'scope': scope, 'settings': settings})

    async def clear_autosave_settings_exceptions(self) -> Ok:
        """
        description Clears the list of all autosave settings exceptions. The method is guaranteed to work only after at least one call to getAutosaveSettings
        """
        return await self._client.call_method('clearAutosaveSettingsExceptions', {'@type': 'clearAutosaveSettingsExceptions'})

    async def change_web_browser_settings(self, open_external_browser: bool = None, display_close_button: bool = None) -> Ok:
        """
        description Changes web browser settings
        open_external_browser Pass true if links must be opened in an external browser by default
        display_close_button Pass true if a close button must be shown in the in-app browser; for Android app only
        """
        return await self._client.call_method('changeWebBrowserSettings', {'@type': 'changeWebBrowserSettings', 'open_external_browser': open_external_browser, 'display_close_button': display_close_button})

    async def add_web_browser_settings_exception(self, open_external_browser: bool = None, url: str = None) -> Ok:
        """
        description Adds a special handling for the opening of the specified URL
        open_external_browser Pass true if the specified website must be opened in an external browser; pass false to open it in the in-app browser. There can be at most 100 exceptions in each list of the exceptions
        url URL of the website
        """
        return await self._client.call_method('addWebBrowserSettingsException', {'@type': 'addWebBrowserSettingsException', 'open_external_browser': open_external_browser, 'url': url})

    async def remove_web_browser_settings_exception(self, url: str = None) -> Ok:
        """
        description Removes a special handling for the opening of the specified URL @url URL of the website
        """
        return await self._client.call_method('removeWebBrowserSettingsException', {'@type': 'removeWebBrowserSettingsException', 'url': url})

    async def remove_all_web_browser_settings_exceptions(self) -> Ok:
        """
        description Removes special handling for the opening of all links
        """
        return await self._client.call_method('removeAllWebBrowserSettingsExceptions', {'@type': 'removeAllWebBrowserSettingsExceptions'})

    async def get_bank_card_info(self, bank_card_number: str = None) -> BankCardInfo:
        """
        description Returns information about a bank card @bank_card_number The bank card number
        """
        return await self._client.call_method('getBankCardInfo', {'@type': 'getBankCardInfo', 'bank_card_number': bank_card_number})

    async def get_passport_element(self, type: PassportElementType = None, password: str = None) -> PassportElement:
        """
        description Returns one of the available Telegram Passport elements @type Telegram Passport element type @password The 2-step verification password of the current user
        """
        return await self._client.call_method('getPassportElement', {'@type': 'getPassportElement', 'type': type, 'password': password})

    async def get_all_passport_elements(self, password: str = None) -> PassportElements:
        """
        description Returns all available Telegram Passport elements @password The 2-step verification password of the current user
        """
        return await self._client.call_method('getAllPassportElements', {'@type': 'getAllPassportElements', 'password': password})

    async def set_passport_element(self, element: InputPassportElement = None, password: str = None) -> PassportElement:
        """
        description Adds an element to the user's Telegram Passport. May return an error with a message "PHONE_VERIFICATION_NEEDED" or "EMAIL_VERIFICATION_NEEDED" if the chosen phone number or the chosen email address must be verified first
        element Input Telegram Passport element
        password The 2-step verification password of the current user
        """
        return await self._client.call_method('setPassportElement', {'@type': 'setPassportElement', 'element': element, 'password': password})

    async def delete_passport_element(self, type: PassportElementType = None) -> Ok:
        """
        description Deletes a Telegram Passport element @type Element type
        """
        return await self._client.call_method('deletePassportElement', {'@type': 'deletePassportElement', 'type': type})

    async def set_passport_element_errors(self, user_id: int = None, errors: List[inputPassportElementError] = None) -> Ok:
        """
        description Informs the user that some of the elements in their Telegram Passport contain errors; for bots only. The user will not be able to resend the elements, until the errors are fixed @user_id User identifier @errors The errors
        """
        return await self._client.call_method('setPassportElementErrors', {'@type': 'setPassportElementErrors', 'user_id': user_id, 'errors': errors})

    async def get_preferred_country_language(self, country_code: str = None) -> Text:
        """
        description Returns an IETF language tag of the language preferred in the country, which must be used to fill native fields in Telegram Passport personal details. Returns a 404 error if unknown @country_code A two-letter ISO 3166-1 alpha-2 country code
        """
        return await self._client.call_method('getPreferredCountryLanguage', {'@type': 'getPreferredCountryLanguage', 'country_code': country_code})

    async def send_email_address_verification_code(self, email_address: str = None) -> EmailAddressAuthenticationCodeInfo:
        """
        description Sends a code to verify an email address to be added to a user's Telegram Passport @email_address Email address
        """
        return await self._client.call_method('sendEmailAddressVerificationCode', {'@type': 'sendEmailAddressVerificationCode', 'email_address': email_address})

    async def resend_email_address_verification_code(self) -> EmailAddressAuthenticationCodeInfo:
        """
        description Resends the code to verify an email address to be added to a user's Telegram Passport
        """
        return await self._client.call_method('resendEmailAddressVerificationCode', {'@type': 'resendEmailAddressVerificationCode'})

    async def check_email_address_verification_code(self, code: str = None) -> Ok:
        """
        description Checks the email address verification code for Telegram Passport @code Verification code to check
        """
        return await self._client.call_method('checkEmailAddressVerificationCode', {'@type': 'checkEmailAddressVerificationCode', 'code': code})

    async def get_passport_authorization_form(self, bot_user_id: int = None, scope: str = None, public_key: str = None, nonce: str = None) -> PassportAuthorizationForm:
        """
        description Returns a Telegram Passport authorization form for sharing data with a service
        bot_user_id User identifier of the service's bot
        scope Telegram Passport element types requested by the service
        public_key Service's public key
        nonce Unique request identifier provided by the service
        """
        return await self._client.call_method('getPassportAuthorizationForm', {'@type': 'getPassportAuthorizationForm', 'bot_user_id': bot_user_id, 'scope': scope, 'public_key': public_key, 'nonce': nonce})

    async def get_passport_authorization_form_available_elements(self, authorization_form_id: int = None, password: str = None) -> PassportElementsWithErrors:
        """
        description Returns already available Telegram Passport elements suitable for completing a Telegram Passport authorization form. Result can be received only once for each authorization form
        authorization_form_id Authorization form identifier
        password The 2-step verification password of the current user
        """
        return await self._client.call_method('getPassportAuthorizationFormAvailableElements', {'@type': 'getPassportAuthorizationFormAvailableElements', 'authorization_form_id': authorization_form_id, 'password': password})

    async def send_passport_authorization_form(self, authorization_form_id: int = None, types: List[PassportElementType] = None) -> Ok:
        """
        description Sends a Telegram Passport authorization form, effectively sharing data with the service. This method must be called after getPassportAuthorizationFormAvailableElements if some previously available elements are going to be reused
        authorization_form_id Authorization form identifier
        types Types of Telegram Passport elements chosen by user to complete the authorization form
        """
        return await self._client.call_method('sendPassportAuthorizationForm', {'@type': 'sendPassportAuthorizationForm', 'authorization_form_id': authorization_form_id, 'types': types})

    async def set_bot_updates_status(self, pending_update_count: int = None, error_message: str = None) -> Ok:
        """
        description Informs the server about the number of pending bot updates if they haven't been processed for a long time; for bots only @pending_update_count The number of pending updates @error_message The last error message
        """
        return await self._client.call_method('setBotUpdatesStatus', {'@type': 'setBotUpdatesStatus', 'pending_update_count': pending_update_count, 'error_message': error_message})

    async def upload_sticker_file(self, user_id: int = None, sticker_format: StickerFormat = None, sticker: InputFile = None) -> File:
        """
        description Uploads a file with a sticker; returns the uploaded file
        user_id Sticker file owner; ignored for regular users
        sticker_format Sticker format
        sticker File to upload; must fit in a 512x512 square. For WEBP stickers the file must be in WEBP or PNG format, which will be converted to WEBP server-side.
        """
        return await self._client.call_method('uploadStickerFile', {'@type': 'uploadStickerFile', 'user_id': user_id, 'sticker_format': sticker_format, 'sticker': sticker})

    async def get_suggested_sticker_set_name(self, title: str = None) -> Text:
        """
        description Returns a suggested name for a new sticker set with a given title @title Sticker set title; 1-64 characters
        """
        return await self._client.call_method('getSuggestedStickerSetName', {'@type': 'getSuggestedStickerSetName', 'title': title})

    async def check_sticker_set_name(self, name: str = None) -> CheckStickerSetNameResult:
        """
        description Checks whether a name can be used for a new sticker set @name Name to be checked
        """
        return await self._client.call_method('checkStickerSetName', {'@type': 'checkStickerSetName', 'name': name})

    async def create_new_sticker_set(self, user_id: int = None, title: str = None, name: str = None, sticker_type: StickerType = None, needs_repainting: bool = None, stickers: List[inputSticker] = None, source: str = None) -> StickerSet:
        """
        description Creates a new sticker set. Returns the newly created sticker set
        user_id Sticker set owner; ignored for regular users
        title Sticker set title; 1-64 characters
        name Sticker set name. Can contain only English letters, digits and underscores. Must end with *"_by_<bot username>"* (*<bot_username>* is case insensitive) for bots; 0-64 characters.
        sticker_type Type of the stickers in the set
        needs_repainting Pass true if stickers in the sticker set must be repainted; for custom emoji sticker sets only
        stickers List of stickers to be added to the set; 1-200 stickers for custom emoji sticker sets, and 1-120 stickers otherwise. For TGS stickers, uploadStickerFile must be used before the sticker is shown
        source Source of the sticker set; may be empty if unknown
        """
        return await self._client.call_method('createNewStickerSet', {'@type': 'createNewStickerSet', 'user_id': user_id, 'title': title, 'name': name, 'sticker_type': sticker_type, 'needs_repainting': needs_repainting, 'stickers': stickers, 'source': source})

    async def add_sticker_to_set(self, user_id: int = None, name: str = None, sticker: inputSticker = None) -> Ok:
        """
        description Adds a new sticker to a set
        user_id Sticker set owner; ignored for regular users
        name Sticker set name. The sticker set must be owned by the current user, and contain less than 200 stickers for custom emoji sticker sets and less than 120 otherwise
        sticker Sticker to add to the set
        """
        return await self._client.call_method('addStickerToSet', {'@type': 'addStickerToSet', 'user_id': user_id, 'name': name, 'sticker': sticker})

    async def replace_sticker_in_set(self, user_id: int = None, name: str = None, old_sticker: InputFile = None, new_sticker: inputSticker = None) -> Ok:
        """
        description Replaces existing sticker in a set. The function is equivalent to removeStickerFromSet, then addStickerToSet, then setStickerPositionInSet
        user_id Sticker set owner; ignored for regular users
        name Sticker set name. The sticker set must be owned by the current user
        old_sticker Sticker to remove from the set
        new_sticker Sticker to add to the set
        """
        return await self._client.call_method('replaceStickerInSet', {'@type': 'replaceStickerInSet', 'user_id': user_id, 'name': name, 'old_sticker': old_sticker, 'new_sticker': new_sticker})

    async def set_sticker_set_thumbnail(self, user_id: int = None, name: str = None, thumbnail: InputFile = None, format: StickerFormat = None) -> Ok:
        """
        description Sets a sticker set thumbnail
        user_id Sticker set owner; ignored for regular users
        name Sticker set name. The sticker set must be owned by the current user
        thumbnail Thumbnail to set; pass null to remove the sticker set thumbnail
        format Format of the thumbnail; pass null if thumbnail is removed
        """
        return await self._client.call_method('setStickerSetThumbnail', {'@type': 'setStickerSetThumbnail', 'user_id': user_id, 'name': name, 'thumbnail': thumbnail, 'format': format})

    async def set_custom_emoji_sticker_set_thumbnail(self, name: str = None, custom_emoji_id: int = None) -> Ok:
        """
        description Sets a custom emoji sticker set thumbnail
        name Sticker set name. The sticker set must be owned by the current user
        custom_emoji_id Identifier of the custom emoji from the sticker set, which will be set as sticker set thumbnail; pass 0 to remove the sticker set thumbnail
        """
        return await self._client.call_method('setCustomEmojiStickerSetThumbnail', {'@type': 'setCustomEmojiStickerSetThumbnail', 'name': name, 'custom_emoji_id': custom_emoji_id})

    async def set_sticker_set_title(self, name: str = None, title: str = None) -> Ok:
        """
        description Sets a sticker set title @name Sticker set name. The sticker set must be owned by the current user @title New sticker set title
        """
        return await self._client.call_method('setStickerSetTitle', {'@type': 'setStickerSetTitle', 'name': name, 'title': title})

    async def delete_sticker_set(self, name: str = None) -> Ok:
        """
        description Completely deletes a sticker set @name Sticker set name. The sticker set must be owned by the current user
        """
        return await self._client.call_method('deleteStickerSet', {'@type': 'deleteStickerSet', 'name': name})

    async def set_sticker_position_in_set(self, sticker: InputFile = None, position: int = None) -> Ok:
        """
        description Changes the position of a sticker in the set to which it belongs. The sticker set must be owned by the current user
        sticker Sticker
        position New position of the sticker in the set, 0-based
        """
        return await self._client.call_method('setStickerPositionInSet', {'@type': 'setStickerPositionInSet', 'sticker': sticker, 'position': position})

    async def remove_sticker_from_set(self, sticker: InputFile = None) -> Ok:
        """
        description Removes a sticker from the set to which it belongs. The sticker set must be owned by the current user @sticker Sticker to remove from the set
        """
        return await self._client.call_method('removeStickerFromSet', {'@type': 'removeStickerFromSet', 'sticker': sticker})

    async def set_sticker_emojis(self, sticker: InputFile = None, emojis: str = None) -> Ok:
        """
        description Changes the list of emojis corresponding to a sticker. The sticker must belong to a regular or custom emoji sticker set that is owned by the current user
        sticker Sticker
        emojis New string with 1-20 emoji corresponding to the sticker
        """
        return await self._client.call_method('setStickerEmojis', {'@type': 'setStickerEmojis', 'sticker': sticker, 'emojis': emojis})

    async def set_sticker_keywords(self, sticker: InputFile = None, keywords: List[str] = None) -> Ok:
        """
        description Changes the list of keywords of a sticker. The sticker must belong to a regular or custom emoji sticker set that is owned by the current user
        sticker Sticker
        keywords List of up to 20 keywords with total length up to 64 characters, which can be used to find the sticker
        """
        return await self._client.call_method('setStickerKeywords', {'@type': 'setStickerKeywords', 'sticker': sticker, 'keywords': keywords})

    async def set_sticker_mask_position(self, sticker: InputFile = None, mask_position: maskPosition = None) -> Ok:
        """
        description Changes the mask position of a mask sticker. The sticker must belong to a mask sticker set that is owned by the current user
        sticker Sticker
        mask_position Position where the mask is placed; pass null to remove mask position
        """
        return await self._client.call_method('setStickerMaskPosition', {'@type': 'setStickerMaskPosition', 'sticker': sticker, 'mask_position': mask_position})

    async def get_owned_sticker_sets(self, offset_sticker_set_id: int = None, limit: int = None) -> StickerSets:
        """
        description Returns sticker sets owned by the current user
        offset_sticker_set_id Identifier of the sticker set from which to return owned sticker sets; use 0 to get results from the beginning
        limit The maximum number of sticker sets to be returned; must be positive and can't be greater than 100. For optimal performance, the number of returned objects is chosen by TDLib and can be smaller than the specified limit
        """
        return await self._client.call_method('getOwnedStickerSets', {'@type': 'getOwnedStickerSets', 'offset_sticker_set_id': offset_sticker_set_id, 'limit': limit})

    async def get_map_thumbnail_file(self, location: location = None, zoom: int = None, width: int = None, height: int = None, scale: int = None, chat_id: int = None) -> File:
        """
        description Returns information about a file with a map thumbnail in PNG format. Only map thumbnail files with size less than 1MB can be downloaded
        location Location of the map center
        zoom Map zoom level; 13-20
        width Map width in pixels before applying scale; 16-1024
        height Map height in pixels before applying scale; 16-1024
        scale Map scale; 1-3
        chat_id Identifier of a chat in which the thumbnail will be shown. Use 0 if unknown
        """
        return await self._client.call_method('getMapThumbnailFile', {'@type': 'getMapThumbnailFile', 'location': location, 'zoom': zoom, 'width': width, 'height': height, 'scale': scale, 'chat_id': chat_id})

    async def get_premium_limit(self, limit_type: PremiumLimitType = None) -> PremiumLimit:
        """
        description Returns information about a limit, increased for Premium users. Returns a 404 error if the limit is unknown @limit_type Type of the limit
        """
        return await self._client.call_method('getPremiumLimit', {'@type': 'getPremiumLimit', 'limit_type': limit_type})

    async def get_premium_features(self, source: PremiumSource = None) -> PremiumFeatures:
        """
        description Returns information about features, available to Premium users @source Source of the request; pass null if the method is called from some non-standard source
        """
        return await self._client.call_method('getPremiumFeatures', {'@type': 'getPremiumFeatures', 'source': source})

    async def get_premium_sticker_examples(self) -> Stickers:
        """
        description Returns examples of premium stickers for demonstration purposes
        """
        return await self._client.call_method('getPremiumStickerExamples', {'@type': 'getPremiumStickerExamples'})

    async def get_premium_info_sticker(self, month_count: int = None) -> Sticker:
        """
        description Returns the sticker to be used as representation of the Telegram Premium subscription @month_count Number of months the Telegram Premium subscription will be active
        """
        return await self._client.call_method('getPremiumInfoSticker', {'@type': 'getPremiumInfoSticker', 'month_count': month_count})

    async def view_premium_feature(self, feature: PremiumFeature = None) -> Ok:
        """
        description Informs TDLib that the user viewed detailed information about a Premium feature on the Premium features screen @feature The viewed premium feature
        """
        return await self._client.call_method('viewPremiumFeature', {'@type': 'viewPremiumFeature', 'feature': feature})

    async def click_premium_subscription_button(self) -> Ok:
        """
        description Informs TDLib that the user clicked Premium subscription button on the Premium features screen
        """
        return await self._client.call_method('clickPremiumSubscriptionButton', {'@type': 'clickPremiumSubscriptionButton'})

    async def get_premium_state(self) -> PremiumState:
        """
        description Returns state of Telegram Premium subscription and promotion videos for Premium features
        """
        return await self._client.call_method('getPremiumState', {'@type': 'getPremiumState'})

    async def get_premium_gift_payment_options(self) -> PremiumGiftPaymentOptions:
        """
        description Returns available options for gifting Telegram Premium to a user
        """
        return await self._client.call_method('getPremiumGiftPaymentOptions', {'@type': 'getPremiumGiftPaymentOptions'})

    async def get_premium_giveaway_payment_options(self, boosted_chat_id: int = None) -> PremiumGiveawayPaymentOptions:
        """
        description Returns available options for creating of Telegram Premium giveaway or manual distribution of Telegram Premium among chat members
        boosted_chat_id Identifier of the supergroup or channel chat, which will be automatically boosted by receivers of the gift codes and which is administered by the user
        """
        return await self._client.call_method('getPremiumGiveawayPaymentOptions', {'@type': 'getPremiumGiveawayPaymentOptions', 'boosted_chat_id': boosted_chat_id})

    async def check_premium_gift_code(self, code: str = None) -> PremiumGiftCodeInfo:
        """
        description Returns information about a Telegram Premium gift code @code The code to check
        """
        return await self._client.call_method('checkPremiumGiftCode', {'@type': 'checkPremiumGiftCode', 'code': code})

    async def apply_premium_gift_code(self, code: str = None) -> Ok:
        """
        description Applies a Telegram Premium gift code @code The code to apply
        """
        return await self._client.call_method('applyPremiumGiftCode', {'@type': 'applyPremiumGiftCode', 'code': code})

    async def gift_premium_with_stars(self, user_id: int = None, star_count: int = None, month_count: int = None, text: formattedText = None) -> Ok:
        """
        description Allows to buy a Telegram Premium subscription for another user with payment in Telegram Stars; for bots only
        user_id Identifier of the user which will receive Telegram Premium
        star_count The number of Telegram Stars to pay for subscription
        month_count Number of months the Telegram Premium subscription will be active for the user
        text Text to show to the user receiving Telegram Premium; 0-getOption("gift_text_length_max") characters. Only Bold, Italic, Underline, Strikethrough, Spoiler, CustomEmoji, and DateTime entities are allowed
        """
        return await self._client.call_method('giftPremiumWithStars', {'@type': 'giftPremiumWithStars', 'user_id': user_id, 'star_count': star_count, 'month_count': month_count, 'text': text})

    async def launch_prepaid_giveaway(self, giveaway_id: int = None, parameters: giveawayParameters = None, winner_count: int = None, star_count: int = None) -> Ok:
        """
        description Launches a prepaid giveaway
        giveaway_id Unique identifier of the prepaid giveaway
        parameters Giveaway parameters
        winner_count The number of users to receive giveaway prize
        star_count The number of Telegram Stars to be distributed through the giveaway; pass 0 for Telegram Premium giveaways
        """
        return await self._client.call_method('launchPrepaidGiveaway', {'@type': 'launchPrepaidGiveaway', 'giveaway_id': giveaway_id, 'parameters': parameters, 'winner_count': winner_count, 'star_count': star_count})

    async def get_giveaway_info(self, chat_id: int = None, message_id: int = None) -> GiveawayInfo:
        """
        description Returns information about a giveaway
        chat_id Identifier of the channel chat which started the giveaway
        message_id Identifier of the giveaway or a giveaway winners message in the chat
        """
        return await self._client.call_method('getGiveawayInfo', {'@type': 'getGiveawayInfo', 'chat_id': chat_id, 'message_id': message_id})

    async def get_star_payment_options(self) -> StarPaymentOptions:
        """
        description Returns available options for Telegram Stars purchase
        """
        return await self._client.call_method('getStarPaymentOptions', {'@type': 'getStarPaymentOptions'})

    async def get_star_gift_payment_options(self, user_id: int = None) -> StarPaymentOptions:
        """
        description Returns available options for Telegram Stars gifting @user_id Identifier of the user who will receive Telegram Stars; pass 0 to get options for an unspecified user
        """
        return await self._client.call_method('getStarGiftPaymentOptions', {'@type': 'getStarGiftPaymentOptions', 'user_id': user_id})

    async def get_star_giveaway_payment_options(self) -> StarGiveawayPaymentOptions:
        """
        description Returns available options for Telegram Star giveaway creation
        """
        return await self._client.call_method('getStarGiveawayPaymentOptions', {'@type': 'getStarGiveawayPaymentOptions'})

    async def get_star_transactions(self, owner_id: MessageSender = None, subscription_id: str = None, direction: TransactionDirection = None, offset: str = None, limit: int = None) -> StarTransactions:
        """
        description Returns the list of Telegram Star transactions for the specified owner
        owner_id Identifier of the owner of the Telegram Stars; can be the identifier of the current user, identifier of an owned bot,
        subscription_id If non-empty, only transactions related to the Star Subscription will be returned
        direction Direction of the transactions to receive; pass null to get all transactions
        offset Offset of the first transaction to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of transactions to return
        """
        return await self._client.call_method('getStarTransactions', {'@type': 'getStarTransactions', 'owner_id': owner_id, 'subscription_id': subscription_id, 'direction': direction, 'offset': offset, 'limit': limit})

    async def get_star_subscriptions(self, only_expiring: bool = None, offset: str = None) -> StarSubscriptions:
        """
        description Returns the list of Telegram Star subscriptions for the current user
        only_expiring Pass true to receive only expiring subscriptions for which there aren't enough Telegram Stars to extend
        offset Offset of the first subscription to return as received from the previous request; use empty string to get the first chunk of results
        """
        return await self._client.call_method('getStarSubscriptions', {'@type': 'getStarSubscriptions', 'only_expiring': only_expiring, 'offset': offset})

    async def can_purchase_from_store(self, purpose: StorePaymentPurpose = None) -> Ok:
        """
        description Checks whether an in-store purchase is possible. Must be called before any in-store purchase. For official applications only @purpose Transaction purpose
        """
        return await self._client.call_method('canPurchaseFromStore', {'@type': 'canPurchaseFromStore', 'purpose': purpose})

    async def assign_store_transaction(self, transaction: StoreTransaction = None, purpose: StorePaymentPurpose = None) -> Ok:
        """
        description Informs server about an in-store purchase. For official applications only @transaction Information about the transaction @purpose Transaction purpose
        """
        return await self._client.call_method('assignStoreTransaction', {'@type': 'assignStoreTransaction', 'transaction': transaction, 'purpose': purpose})

    async def edit_star_subscription(self, subscription_id: str = None, is_canceled: bool = None) -> Ok:
        """
        description Cancels or re-enables Telegram Star subscription
        subscription_id Identifier of the subscription to change
        is_canceled New value of is_canceled
        """
        return await self._client.call_method('editStarSubscription', {'@type': 'editStarSubscription', 'subscription_id': subscription_id, 'is_canceled': is_canceled})

    async def edit_user_star_subscription(self, user_id: int = None, telegram_payment_charge_id: str = None, is_canceled: bool = None) -> Ok:
        """
        description Cancels or re-enables Telegram Star subscription for a user; for bots only
        user_id User identifier
        telegram_payment_charge_id Telegram payment identifier of the subscription
        is_canceled Pass true to cancel the subscription; pass false to allow the user to enable it
        """
        return await self._client.call_method('editUserStarSubscription', {'@type': 'editUserStarSubscription', 'user_id': user_id, 'telegram_payment_charge_id': telegram_payment_charge_id, 'is_canceled': is_canceled})

    async def reuse_star_subscription(self, subscription_id: str = None) -> Ok:
        """
        description Reuses an active Telegram Star subscription to a channel chat and joins the chat again @subscription_id Identifier of the subscription
        """
        return await self._client.call_method('reuseStarSubscription', {'@type': 'reuseStarSubscription', 'subscription_id': subscription_id})

    async def set_chat_affiliate_program(self, chat_id: int = None, parameters: affiliateProgramParameters = None) -> Ok:
        """
        description Changes affiliate program for a bot
        chat_id Identifier of the chat with an owned bot for which affiliate program is changed
        parameters Parameters of the affiliate program; pass null to close the currently active program. If there is an active program, then commission and program duration can only be increased.
        """
        return await self._client.call_method('setChatAffiliateProgram', {'@type': 'setChatAffiliateProgram', 'chat_id': chat_id, 'parameters': parameters})

    async def search_chat_affiliate_program(self, username: str = None, referrer: str = None) -> Chat:
        """
        description Searches a chat with an affiliate program. Returns the chat if found and the program is active
        username Username of the chat
        referrer The referrer from an internalLinkTypeChatAffiliateProgram link
        """
        return await self._client.call_method('searchChatAffiliateProgram', {'@type': 'searchChatAffiliateProgram', 'username': username, 'referrer': referrer})

    async def search_affiliate_programs(self, affiliate: AffiliateType = None, sort_order: AffiliateProgramSortOrder = None, offset: str = None, limit: int = None) -> FoundAffiliatePrograms:
        """
        description Searches affiliate programs that can be connected to the given affiliate
        affiliate The affiliate for which affiliate programs are searched for
        sort_order Sort order for the results
        offset Offset of the first affiliate program to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of affiliate programs to return
        """
        return await self._client.call_method('searchAffiliatePrograms', {'@type': 'searchAffiliatePrograms', 'affiliate': affiliate, 'sort_order': sort_order, 'offset': offset, 'limit': limit})

    async def connect_affiliate_program(self, affiliate: AffiliateType = None, bot_user_id: int = None) -> ConnectedAffiliateProgram:
        """
        description Connects an affiliate program to the given affiliate. Returns information about the connected affiliate program
        affiliate The affiliate to which the affiliate program will be connected
        bot_user_id Identifier of the bot, which affiliate program is connected
        """
        return await self._client.call_method('connectAffiliateProgram', {'@type': 'connectAffiliateProgram', 'affiliate': affiliate, 'bot_user_id': bot_user_id})

    async def disconnect_affiliate_program(self, affiliate: AffiliateType = None, url: str = None) -> ConnectedAffiliateProgram:
        """
        description Disconnects an affiliate program from the given affiliate and immediately deactivates its referral link. Returns updated information about the disconnected affiliate program
        affiliate The affiliate to which the affiliate program is connected
        url The referral link of the affiliate program
        """
        return await self._client.call_method('disconnectAffiliateProgram', {'@type': 'disconnectAffiliateProgram', 'affiliate': affiliate, 'url': url})

    async def get_connected_affiliate_program(self, affiliate: AffiliateType = None, bot_user_id: int = None) -> ConnectedAffiliateProgram:
        """
        description Returns an affiliate program that was connected to the given affiliate by identifier of the bot that created the program
        affiliate The affiliate to which the affiliate program will be connected
        bot_user_id Identifier of the bot that created the program
        """
        return await self._client.call_method('getConnectedAffiliateProgram', {'@type': 'getConnectedAffiliateProgram', 'affiliate': affiliate, 'bot_user_id': bot_user_id})

    async def get_connected_affiliate_programs(self, affiliate: AffiliateType = None, offset: str = None, limit: int = None) -> ConnectedAffiliatePrograms:
        """
        description Returns affiliate programs that were connected to the given affiliate
        affiliate The affiliate to which the affiliate programs were connected
        offset Offset of the first affiliate program to return as received from the previous request; use empty string to get the first chunk of results
        limit The maximum number of affiliate programs to return
        """
        return await self._client.call_method('getConnectedAffiliatePrograms', {'@type': 'getConnectedAffiliatePrograms', 'affiliate': affiliate, 'offset': offset, 'limit': limit})

    async def get_business_features(self, source: BusinessFeature = None) -> BusinessFeatures:
        """
        description Returns information about features, available to Business users @source Source of the request; pass null if the method is called from settings or some non-standard source
        """
        return await self._client.call_method('getBusinessFeatures', {'@type': 'getBusinessFeatures', 'source': source})

    async def accept_terms_of_service(self, terms_of_service_id: str = None) -> Ok:
        """
        description Accepts Telegram terms of service @terms_of_service_id Terms of service identifier
        """
        return await self._client.call_method('acceptTermsOfService', {'@type': 'acceptTermsOfService', 'terms_of_service_id': terms_of_service_id})

    async def search_strings_by_prefix(self, strings: List[str] = None, query: str = None, limit: int = None, return_none_for_empty_query: bool = None) -> FoundPositions:
        """
        description Searches specified query by word prefixes in the provided strings. Returns 0-based positions of strings that matched. Can be called synchronously
        strings The strings to search in for the query
        query Query to search for
        limit The maximum number of objects to return
        return_none_for_empty_query Pass true to receive no results for an empty query
        """
        return await self._client.call_method('searchStringsByPrefix', {'@type': 'searchStringsByPrefix', 'strings': strings, 'query': query, 'limit': limit, 'return_none_for_empty_query': return_none_for_empty_query})

    async def send_custom_request(self, method: str = None, parameters: str = None) -> CustomRequestResult:
        """
        description Sends a custom request; for bots only @method The method name @parameters JSON-serialized method parameters
        """
        return await self._client.call_method('sendCustomRequest', {'@type': 'sendCustomRequest', 'method': method, 'parameters': parameters})

    async def answer_custom_query(self, custom_query_id: int = None, data: str = None) -> Ok:
        """
        description Answers a custom query; for bots only @custom_query_id Identifier of a custom query @data JSON-serialized answer to the query
        """
        return await self._client.call_method('answerCustomQuery', {'@type': 'answerCustomQuery', 'custom_query_id': custom_query_id, 'data': data})

    async def set_alarm(self, seconds: float = None) -> Ok:
        """
        description Succeeds after a specified amount of time has passed. Can be called before initialization @seconds Number of seconds before the function returns
        """
        return await self._client.call_method('setAlarm', {'@type': 'setAlarm', 'seconds': seconds})

    async def get_countries(self) -> Countries:
        """
        description Returns information about existing countries. Can be called before authorization
        """
        return await self._client.call_method('getCountries', {'@type': 'getCountries'})

    async def get_country(self, country_code: str = None) -> CountryInfo:
        """
        description Returns information about an existing country. Can be called before authorization @country_code A two-letter ISO 3166-1 alpha-2 country code
        """
        return await self._client.call_method('getCountry', {'@type': 'getCountry', 'country_code': country_code})

    async def get_country_code(self) -> Text:
        """
        description Uses the current IP address to find the current country. Returns two-letter ISO 3166-1 alpha-2 country code. Can be called before authorization
        """
        return await self._client.call_method('getCountryCode', {'@type': 'getCountryCode'})

    async def get_phone_number_info(self, phone_number_prefix: str = None) -> PhoneNumberInfo:
        """
        description Returns information about a phone number by its prefix. Can be called before authorization @phone_number_prefix The phone number prefix
        """
        return await self._client.call_method('getPhoneNumberInfo', {'@type': 'getPhoneNumberInfo', 'phone_number_prefix': phone_number_prefix})

    async def get_phone_number_info_sync(self, language_code: str = None, phone_number_prefix: str = None) -> PhoneNumberInfo:
        """
        description Returns information about a phone number by its prefix synchronously. getCountries must be called at least once after changing localization to the specified language if properly localized country information is expected. Can be called synchronously
        language_code A two-letter ISO 639-1 language code for country information localization
        phone_number_prefix The phone number prefix
        """
        return await self._client.call_method('getPhoneNumberInfoSync', {'@type': 'getPhoneNumberInfoSync', 'language_code': language_code, 'phone_number_prefix': phone_number_prefix})

    async def get_collectible_item_info(self, type: CollectibleItemType = None) -> CollectibleItemInfo:
        """
        description Returns information about a given collectible item that was purchased at https://fragment.com
        type Type of the collectible item. The item must be used by a user and must be visible to the current user
        """
        return await self._client.call_method('getCollectibleItemInfo', {'@type': 'getCollectibleItemInfo', 'type': type})

    async def get_deep_link_info(self, link: str = None) -> DeepLinkInfo:
        """
        description Returns information about a tg:// deep link. Use "tg://need_update_for_some_feature" or "tg:some_unsupported_feature" for testing. Returns a 404 error for unknown links. Can be called before authorization @link The link
        """
        return await self._client.call_method('getDeepLinkInfo', {'@type': 'getDeepLinkInfo', 'link': link})

    async def get_application_config(self) -> JsonValue:
        """
        description Returns application config, provided by the server. Can be called before authorization
        """
        return await self._client.call_method('getApplicationConfig', {'@type': 'getApplicationConfig'})

    async def save_application_log_event(self, type: str = None, chat_id: int = None, data: JsonValue = None) -> Ok:
        """
        description Saves application log event on the server. Can be called before authorization @type Event type @chat_id Optional chat identifier, associated with the event @data The log event data
        """
        return await self._client.call_method('saveApplicationLogEvent', {'@type': 'saveApplicationLogEvent', 'type': type, 'chat_id': chat_id, 'data': data})

    async def get_application_download_link(self) -> HttpUrl:
        """
        description Returns the link for downloading official Telegram application to be used when the current user invites friends to Telegram
        """
        return await self._client.call_method('getApplicationDownloadLink', {'@type': 'getApplicationDownloadLink'})

    async def add_proxy(self, proxy: proxy = None, enable: bool = None, comment: str = None) -> AddedProxy:
        """
        description Adds a proxy server for network requests. Can be called before authorization
        proxy The proxy to add
        enable Pass true to immediately enable the proxy
        comment Comment to set for the proxy
        """
        return await self._client.call_method('addProxy', {'@type': 'addProxy', 'proxy': proxy, 'enable': enable, 'comment': comment})

    async def edit_proxy(self, proxy_id: int = None, proxy: proxy = None, enable: bool = None, comment: str = None) -> AddedProxy:
        """
        description Edits an existing proxy server for network requests. Can be called before authorization
        proxy_id Proxy identifier
        proxy The new information about the proxy
        enable Pass true to immediately enable the proxy
        comment New comment for the proxy
        """
        return await self._client.call_method('editProxy', {'@type': 'editProxy', 'proxy_id': proxy_id, 'proxy': proxy, 'enable': enable, 'comment': comment})

    async def enable_proxy(self, proxy_id: int = None) -> Ok:
        """
        description Enables a proxy. Only one proxy can be enabled at a time. Can be called before authorization @proxy_id Proxy identifier
        """
        return await self._client.call_method('enableProxy', {'@type': 'enableProxy', 'proxy_id': proxy_id})

    async def disable_proxy(self) -> Ok:
        """
        description Disables the currently enabled proxy. Can be called before authorization
        """
        return await self._client.call_method('disableProxy', {'@type': 'disableProxy'})

    async def remove_proxy(self, proxy_id: int = None) -> Ok:
        """
        description Removes a proxy server. Can be called before authorization @proxy_id Proxy identifier
        """
        return await self._client.call_method('removeProxy', {'@type': 'removeProxy', 'proxy_id': proxy_id})

    async def get_proxies(self) -> AddedProxies:
        """
        description Returns the list of proxies that are currently set up. Can be called before authorization
        """
        return await self._client.call_method('getProxies', {'@type': 'getProxies'})

    async def ping_proxy(self, proxy: proxy = None) -> Seconds:
        """
        description Computes time needed to receive a response from a Telegram server through a proxy. Can be called before authorization
        proxy The proxy to test; pass null to ping a Telegram server without a proxy
        """
        return await self._client.call_method('pingProxy', {'@type': 'pingProxy', 'proxy': proxy})

    async def set_log_stream(self, log_stream: LogStream = None) -> Ok:
        """
        description Sets new log stream for internal logging of TDLib. Can be called synchronously @log_stream New log stream
        """
        return await self._client.call_method('setLogStream', {'@type': 'setLogStream', 'log_stream': log_stream})

    async def get_log_stream(self) -> LogStream:
        """
        description Returns information about currently used log stream for internal logging of TDLib. Can be called synchronously
        """
        return await self._client.call_method('getLogStream', {'@type': 'getLogStream'})

    async def set_log_verbosity_level(self, new_verbosity_level: int = None) -> Ok:
        """
        description Sets the verbosity level of the internal logging of TDLib. Can be called synchronously
        new_verbosity_level New value of the verbosity level for logging. Value 0 corresponds to fatal errors, value 1 corresponds to errors, value 2 corresponds to warnings and debug warnings,
        """
        return await self._client.call_method('setLogVerbosityLevel', {'@type': 'setLogVerbosityLevel', 'new_verbosity_level': new_verbosity_level})

    async def get_log_verbosity_level(self) -> LogVerbosityLevel:
        """
        description Returns current verbosity level of the internal logging of TDLib. Can be called synchronously
        """
        return await self._client.call_method('getLogVerbosityLevel', {'@type': 'getLogVerbosityLevel'})

    async def get_log_tags(self) -> LogTags:
        """
        description Returns the list of available TDLib internal log tags, for example, ["actor", "binlog", "connections", "notifications", "proxy"]. Can be called synchronously
        """
        return await self._client.call_method('getLogTags', {'@type': 'getLogTags'})

    async def set_log_tag_verbosity_level(self, tag: str = None, new_verbosity_level: int = None) -> Ok:
        """
        description Sets the verbosity level for a specified TDLib internal log tag. Can be called synchronously
        tag Logging tag to change verbosity level
        new_verbosity_level New verbosity level; 1-1024
        """
        return await self._client.call_method('setLogTagVerbosityLevel', {'@type': 'setLogTagVerbosityLevel', 'tag': tag, 'new_verbosity_level': new_verbosity_level})

    async def get_log_tag_verbosity_level(self, tag: str = None) -> LogVerbosityLevel:
        """
        description Returns current verbosity level for a specified TDLib internal log tag. Can be called synchronously @tag Logging tag to change verbosity level
        """
        return await self._client.call_method('getLogTagVerbosityLevel', {'@type': 'getLogTagVerbosityLevel', 'tag': tag})

    async def add_log_message(self, verbosity_level: int = None, text: str = None) -> Ok:
        """
        description Adds a message to TDLib internal log. Can be called synchronously
        verbosity_level The minimum verbosity level needed for the message to be logged; 0-1023
        text Text of a message to log
        """
        return await self._client.call_method('addLogMessage', {'@type': 'addLogMessage', 'verbosity_level': verbosity_level, 'text': text})

    async def get_user_support_info(self, user_id: int = None) -> UserSupportInfo:
        """
        description Returns support information for the given user; for Telegram support only @user_id User identifier
        """
        return await self._client.call_method('getUserSupportInfo', {'@type': 'getUserSupportInfo', 'user_id': user_id})

    async def set_user_support_info(self, user_id: int = None, message: formattedText = None) -> UserSupportInfo:
        """
        description Sets support information for the given user; for Telegram support only @user_id User identifier @message New information message
        """
        return await self._client.call_method('setUserSupportInfo', {'@type': 'setUserSupportInfo', 'user_id': user_id, 'message': message})

    async def get_support_name(self) -> Text:
        """
        description Returns localized name of the Telegram support user; for Telegram support only
        """
        return await self._client.call_method('getSupportName', {'@type': 'getSupportName'})

    async def test_call_empty(self) -> Ok:
        """
        description Does nothing; for testing only. This is an offline method. Can be called before authorization
        """
        return await self._client.call_method('testCallEmpty', {'@type': 'testCallEmpty'})

    async def test_call_string(self, x: str = None) -> TestString:
        """
        description Returns the received string; for testing only. This is an offline method. Can be called before authorization @x String to return
        """
        return await self._client.call_method('testCallString', {'@type': 'testCallString', 'x': x})

    async def test_call_bytes(self, x: bytes = None) -> TestBytes:
        """
        description Returns the received bytes; for testing only. This is an offline method. Can be called before authorization @x Bytes to return
        """
        return await self._client.call_method('testCallBytes', {'@type': 'testCallBytes', 'x': x})

    async def test_call_vector_int(self, x: List[int] = None) -> TestVectorInt:
        """
        description Returns the received vector of numbers; for testing only. This is an offline method. Can be called before authorization @x Vector of numbers to return
        """
        return await self._client.call_method('testCallVectorInt', {'@type': 'testCallVectorInt', 'x': x})

    async def test_call_vector_int_object(self, x: List[testInt] = None) -> TestVectorIntObject:
        """
        description Returns the received vector of objects containing a number; for testing only. This is an offline method. Can be called before authorization @x Vector of objects to return
        """
        return await self._client.call_method('testCallVectorIntObject', {'@type': 'testCallVectorIntObject', 'x': x})

    async def test_call_vector_string(self, x: List[str] = None) -> TestVectorString:
        """
        description Returns the received vector of strings; for testing only. This is an offline method. Can be called before authorization @x Vector of strings to return
        """
        return await self._client.call_method('testCallVectorString', {'@type': 'testCallVectorString', 'x': x})

    async def test_call_vector_string_object(self, x: List[testString] = None) -> TestVectorStringObject:
        """
        description Returns the received vector of objects containing a string; for testing only. This is an offline method. Can be called before authorization @x Vector of objects to return
        """
        return await self._client.call_method('testCallVectorStringObject', {'@type': 'testCallVectorStringObject', 'x': x})

    async def test_square_int(self, x: int = None) -> TestInt:
        """
        description Returns the squared received number; for testing only. This is an offline method. Can be called before authorization @x Number to square
        """
        return await self._client.call_method('testSquareInt', {'@type': 'testSquareInt', 'x': x})

    async def test_network(self) -> Ok:
        """
        description Sends a simple network request to the Telegram servers; for testing only. Can be called before authorization
        """
        return await self._client.call_method('testNetwork', {'@type': 'testNetwork'})

    async def test_proxy(self, proxy: proxy = None, dc_id: int = None, timeout: float = None) -> Ok:
        """
        description Sends a simple network request to the Telegram servers via proxy; for testing only. Can be called before authorization
        proxy The proxy to test
        dc_id Identifier of a datacenter with which to test connection
        timeout The maximum overall timeout for the request
        """
        return await self._client.call_method('testProxy', {'@type': 'testProxy', 'proxy': proxy, 'dc_id': dc_id, 'timeout': timeout})

    async def test_get_difference(self) -> Ok:
        """
        description Forces an updates.getDifference call to the Telegram servers; for testing only
        """
        return await self._client.call_method('testGetDifference', {'@type': 'testGetDifference'})

    async def test_use_update(self) -> Update:
        """
        description Does nothing and ensures that the Update object is used; for testing only. This is an offline method. Can be called before authorization
        """
        return await self._client.call_method('testUseUpdate', {'@type': 'testUseUpdate'})

    async def test_return_error(self, error: error = None) -> Error:
        """
        description Returns the specified error and ensures that the Error object is used; for testing only. Can be called synchronously @error The error to be returned
        """
        return await self._client.call_method('testReturnError', {'@type': 'testReturnError', 'error': error})

