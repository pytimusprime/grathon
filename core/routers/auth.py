from typing import Optional, Any, Callable, TypeAlias

from grathon.core.router import Router

from grathon.core.TLSchema_Manager.tltypes import (
    updateAuthorizationState,
    authorizationStateWaitTdlibParameters,
    authorizationStateWaitPhoneNumber,
    authorizationStateWaitCode,
    authorizationStateWaitPassword,
    authorizationStateReady
)
from grathon.core.contexts.context import Context

AuthStateCtx: TypeAlias = Context[updateAuthorizationState]

class AuthRouter(Router[updateAuthorizationState]):
    """
    """
    def __init__(self) -> None:
        super().__init__(name="AuthRouter")

        self._on_params_cb:Optional[Callable[[AuthStateCtx], Any]] = None
        self._on_phone_cb:Optional[Callable[[AuthStateCtx], Any]] = None
        self._on_token_cb:Optional[Callable[[AuthStateCtx], Any]] = None
        self._on_ready_cb:Optional[Callable[[AuthStateCtx], Any]] = None
        self._on_code_cb:Optional[Callable[[AuthStateCtx], Any]] = None
        self._on_password_cb:Optional[Callable[[AuthStateCtx], Any]] = None
        self._on_other_cb:Optional[Callable[[AuthStateCtx], Any]] = None


        _ = self.on(updateAuthorizationState, callback=self._internal_auth_handler)


    async def _internal_auth_handler(self, ctx:AuthStateCtx):
        state_name = type(ctx.update.authorization_state).__name__
        print(f"[AUTH] Received auth state: {state_name}", flush=True)

        async def _call(cb:Optional[Callable[[AuthStateCtx], Any]]):
            if cb: await cb(ctx)
        match ctx.update.authorization_state:
            case authorizationStateWaitCode():
                await _call(self._on_code_cb)
            case authorizationStateWaitPassword():
                await _call(self._on_password_cb)
            case authorizationStateWaitTdlibParameters():
                await _call(self._on_params_cb)
            case authorizationStateWaitPhoneNumber():
                # If token callback is set, prioritize token
                if self._on_token_cb:
                    await _call(self._on_token_cb)
                # Otherwise if phone callback exists
                elif self._on_phone_cb:
                    await _call(self._on_phone_cb)
                else:
                    # If neither, fall through to general handler
                    await _call(self._on_other_cb)
            case authorizationStateReady():
                await _call(self._on_ready_cb)
            case _:
                await _call(self._on_other_cb)



    def on_params(self, func: Optional[Callable[['AuthStateCtx'], Any]] = None):
        def dec(f: Callable[['AuthStateCtx'], Any]):
            self._on_params_cb = f
            return f

        return dec(func) if func else dec

    def on_phone(self, func: Optional[Callable[['AuthStateCtx'], Any]] = None):
        def dec(f: Callable[['AuthStateCtx'], Any]):
            self._on_phone_cb = f
            return f

        return dec(func) if func else dec

    def on_token(self, func: Optional[Callable[['AuthStateCtx'], Any]] = None)-> (Callable[['AuthStateCtx'], Any] |
                                                                             Callable[[Callable[['AuthStateCtx'], Any]],
                                                                             Callable[['AuthStateCtx'], Any]]):
        def dec(f: Callable[['AuthStateCtx'], Any]):
            self._on_token_cb = f
            return f

        return dec(func) if func else dec

    def on_code(self, func: Optional[Callable[['AuthStateCtx'], Any]] = None):
        def dec(f: Callable[['AuthStateCtx'], Any]):
            self._on_code_cb = f
            return f
        return dec(func) if func else dec

    def on_password(self,func:Optional[Callable[['AuthStateCtx'],Any]]= None):
        def dec(f: Callable[['AuthStateCtx'], Any]):
            self._on_password_cb = f
            return f
        return dec(func) if func else dec

    def on_ready(self, func: Optional[Callable[['AuthStateCtx'], Any]] = None):
        def dec(f: Callable[['AuthStateCtx'], Any]):
            self._on_ready_cb = f
            return f
        return dec(func) if func else dec

    def on_other(self,func:Optional[Callable[['AuthStateCtx'],Any]]= None):
        def dec(f: Callable[['AuthStateCtx'], Any]):
            self._on_other_cb = f
            return f
        return dec(func) if func else dec