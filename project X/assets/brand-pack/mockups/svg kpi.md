Closed Referrals KPI SVG =
VAR _Base =
    [Closed Referrals (by Reason)]
VAR _PriorMonth =
    [Closed Referral Previous Month]
VAR _VariancePct =
    DIVIDE ( _Base - _PriorMonth, _PriorMonth )
VAR _Direction =
    SIGN ( _Base - _PriorMonth )
VAR _Accent =
    SWITCH ( _Direction, 1, "#3A8B6F", -1, "#C82B5E", "#6B6B63" )
VAR _BadgeBg =
    SWITCH ( _Direction, 1, "#E4F3EC", -1, "#FBE4EE", "#F0F0EE" )
VAR _Icon =
    SWITCH (
        _Direction,
        1, "<path d='M186 64 l8 -8 l6 6 l14 -14' stroke='" & _Accent & "' stroke-width='3' fill='none' stroke-linecap='round' stroke-linejoin='round'/><path d='M206 48 L214 48 L214 56' stroke='" & _Accent & "' stroke-width='3' fill='none' stroke-linecap='round' stroke-linejoin='round'/>",
        -1, "<path d='M186 48 l8 8 l6 -6 l14 14' stroke='" & _Accent & "' stroke-width='3' fill='none' stroke-linecap='round' stroke-linejoin='round'/><path d='M206 64 L214 64 L214 56' stroke='" & _Accent & "' stroke-width='3' fill='none' stroke-linecap='round' stroke-linejoin='round'/>",
        "<circle cx='200' cy='56' r='4' fill='" & _Accent & "'/>"
    )
VAR _ValueText =
    FORMAT ( _Base, "#,##0" )
VAR _VarianceText =
    IF (
        ISBLANK ( _PriorMonth ) || _PriorMonth = 0,
        "n/a",
        FORMAT ( _VariancePct * 100, "+0.0;-0.0;0.0" ) & "%25"
    )
VAR _Caption =
    "vs " & FORMAT ( _PriorMonth, "#,##0" ) & " Last month"
VAR _Svg =
    "data:image/svg+xml;utf8," &
    "<svg xmlns='http://www.w3.org/2000/svg' width='320' height='150' viewBox='0 0 320 150'>" &
    "<rect width='320' height='150' rx='16' fill='#FFFFFF' stroke='#E5E0D5' stroke-width='1'/>" &
    "<text x='24' y='34' font-family='Segoe UI' font-size='15' fill='#6B6B63'>Closed Referrals</text>" &
    "<text x='24' y='92' font-family='Segoe UI' font-size='44' font-weight='700' fill='#1C1C1A'>" & _ValueText & "</text>" &
    "<rect x='178' y='34' width='44' height='44' rx='10' fill='" & _BadgeBg & "'/>" &
    _Icon &
    "<text x='232' y='66' font-family='Segoe UI' font-size='20' font-weight='600' fill='" & _Accent & "'>" & _VarianceText & "</text>" &
    "<text x='178' y='96' font-family='Segoe UI' font-size='13' fill='#6B6B63'>" & _Caption & "</text>" &
    "</svg>"
RETURN
    _Svg
